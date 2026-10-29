import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_create_url(client):
    response = client.post(
        "/urls",
        json={"original_url": "https://www.python.org/"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["original_url"] == "https://www.python.org/"
    assert len(data["short_code"]) == 6
    assert data["click_count"] == 0


def test_list_urls(client):
    client.post(
        "/urls",
        json={"original_url": "https://www.python.org/"},
    )

    response = client.get("/urls")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_missing_url(client):
    response = client.get("/urls/99999")

    assert response.status_code == 404


def test_delete_url(client):
    created = client.post(
        "/urls",
        json={"original_url": "https://www.python.org/"},
    ).json()

    response = client.delete(f"/urls/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/urls/{created['id']}").status_code == 404


def test_redirect_increments_click_count(client):
    created = client.post(
        "/urls",
        json={"original_url": "https://www.python.org/"},
    ).json()

    response = client.get(
        f"/{created['short_code']}",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"] == "https://www.python.org/"

    details = client.get(f"/urls/{created['id']}").json()
    assert details["click_count"] == 1


def test_redirect_missing_code(client):
    response = client.get(
        "/notARealCode",
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_list_urls_pagination(client):
    for domain in ("python.org", "fastapi.tiangolo.com", "github.com"):
        response = client.post(
            "/urls",
            json={"original_url": f"https://{domain}/"},
        )
        assert response.status_code == 201

    response = client.get("/urls?skip=0&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_search_urls(client):
    client.post(
        "/urls",
        json={"original_url": "https://www.python.org/"},
    )
    client.post(
        "/urls",
        json={"original_url": "https://www.github.com/"},
    )

    response = client.get("/urls?search=python")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "python.org" in results[0]["original_url"]


def test_list_urls_rejects_invalid_pagination(client):
    assert client.get("/urls?skip=-1").status_code == 422
    assert client.get("/urls?limit=0").status_code == 422
    assert client.get("/urls?limit=101").status_code == 422
