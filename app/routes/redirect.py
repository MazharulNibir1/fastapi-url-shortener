from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.cache import redis_client
from app import crud

router = APIRouter()

@router.get("/{code}")
async def redirect_to_url(code: str, db: AsyncSession = Depends(get_db)):
    cached = await redis_client.get(f"url:{code}")
    if cached:
        await redis_client.incr(f"clicks:{code}")
        return RedirectResponse(cached)

    url_obj = await crud.get_url_by_code(db, code)   # cache miss fallback
    if not url_obj:
        raise HTTPException(status_code=404, detail="Not found")

    await redis_client.set(f"url:{code}", url_obj.long_url)
    await redis_client.incr(f"clicks:{code}")
    return RedirectResponse(url_obj.long_url)