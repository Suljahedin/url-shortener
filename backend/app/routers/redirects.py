from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import URL

router = APIRouter(tags=["Redirects"])


@router.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db),
):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    url.click_count += 1
    db.commit()

    return RedirectResponse(
        url=url.original_url,
        status_code=307,
    )
