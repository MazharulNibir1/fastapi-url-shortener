from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cache import redis_client
from app.schemas import ShortenRequest, ShortenResponse
from app.shortener import generate_code
from app import crud

router = APIRouter()

@router.post("/shorten", response_model=ShortenResponse)
async def shorten_url(payload: ShortenRequest, db: AsyncSession = Depends(get_db)):
    code = generate_code()
    while await crud.get_url_by_code(db, code):   # collision retry
        code = generate_code()

    url_str = str(payload.url)
    await crud.create_url(db, code, url_str)
    await redis_client.set(f"url:{code}", url_str)  # warm cache on write

    return ShortenResponse(code=code, short_url=f"http://localhost:8000/{code}", long_url=url_str)