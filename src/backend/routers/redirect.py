import random, string
from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models, schemas
from .users import get_current_user
from ..database import get_db


router = APIRouter()

@router.get('/{short_code}')
async def redirect(short_code: str, db: AsyncSession = Depends(get_db)):

    link_result = await db.execute(select(models.Link).where(models.Link.short_code == short_code))

    link = link_result.scalar_one_or_none()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ссылка не найдена!'
        )
    
    return RedirectResponse(url=link.original_link)