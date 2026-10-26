import secrets
import string

from sqlalchemy.orm import Session

from app.models import URL
from app.schemas import URLCreate

ALPHABET = string.ascii_letters + string.digits


def create_short_url(db: Session, data: URLCreate) -> URL:
    while True:
        short_code = "".join(secrets.choice(ALPHABET) for _ in range(6))

        existing_url = db.query(URL).filter(URL.short_code == short_code).first()

        if existing_url is None:
            break

    url = URL(
        original_url=str(data.original_url),
        short_code=short_code,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url
