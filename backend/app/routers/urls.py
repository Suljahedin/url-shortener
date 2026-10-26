from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
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
