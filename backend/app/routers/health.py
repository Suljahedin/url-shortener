from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "URL Shortener API is running!"}


@router.get("/health")
def health_check():
    return {"status": "ok"}
