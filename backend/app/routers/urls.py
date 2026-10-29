from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import URL
from app.schemas import URLCreate, URLResponse
from app.services import create_short_url

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post(
    "",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_url(data: URLCreate, db: Session = Depends(get_db)):
    return create_short_url(db, data)


@router.get("", response_model=list[URLResponse])
def get_urls(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, max_length=2048),
    db: Session = Depends(get_db),
):
    query = db.query(URL)

    if search and search.strip():
        query = query.filter(URL.original_url.contains(search.strip()))

    return query.order_by(URL.id.desc()).offset(skip).limit(limit).all()


@router.get("/{url_id}", response_model=URLResponse)
def get_url(url_id: int, db: Session = Depends(get_db)):
    url = db.get(URL, url_id)

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    return url


@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(url_id: int, db: Session = Depends(get_db)):
    url = db.get(URL, url_id)

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found",
        )

    db.delete(url)
    db.commit()
