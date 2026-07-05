from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import URL

async def get_url_by_code(db: AsyncSession, code: str) -> URL | None:
    result = await db.execute(select(URL).where(URL.code == code))
    return result.scalar_one_or_none()

async def create_url(db: AsyncSession, code: str, long_url: str) -> URL:
    url = URL(code = code, long_url=long_url)
    db.add(url)
    await db.commit()
    await db.refresh(url)
    return url
