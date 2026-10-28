import secrets
import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import URL
from app.schemas import URLCreate

ALPHABET = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 6
MAX_ATTEMPTS = 5


def create_short_url(db: Session, data: URLCreate) -> URL:
    for _ in range(MAX_ATTEMPTS):
        short_code = "".join(secrets.choice(ALPHABET) for _ in range(SHORT_CODE_LENGTH))

        existing_url = db.query(URL).filter(URL.short_code == short_code).first()

        if existing_url is not None:
            continue

        url = URL(
            original_url=str(data.original_url),
            short_code=short_code,
        )

        db.add(url)

        try:
            db.commit()
            db.refresh(url)
            return url
        except IntegrityError:
            db.rollback()

    raise RuntimeError("Could not generate a unique short code")
