import redis.asyncio as redis
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from ..database import get_db
from ..client import get_redis_client


router = APIRouter()

@router.get('/{short_code}')
async def redirect(short_code: str, redis_client: redis.Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db)):

    link = await redis_client.get(f'redirect:{short_code}')

    if link:
        print('CACHE HIT')

        await redis_client.incr(f'clicks:{short_code}')

        return RedirectResponse(url=link)
    
    print('CACHE MISS')

    db_link_result = select(models.Link).where(models.Link.short_code == short_code)
    db_link = (await db.execute(db_link_result)).scalar_one_or_none()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ссылка не найдена!'
        )
    
    await redis_client.set(f'redirect:{db_link.short_code}', db_link.original_link)

    await redis_client.incr(f'clicks:{short_code}')
    
    return RedirectResponse(url=db_link.original_link)