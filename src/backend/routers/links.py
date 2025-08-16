import random, string, json
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis.asyncio import Redis
from .. import models, schemas
from .users import get_current_user
from ..database import get_db
from ..client import get_redis_client


router = APIRouter()


def get_short_code(length: int=6):

    alphabet = string.ascii_letters + string.digits

    short_code = "".join(random.choices(alphabet, k=length))
    
    return short_code


@router.post('/links', response_model=schemas.LinkOut, status_code=status.HTTP_201_CREATED)
async def create_short_link(link_data: schemas.LinkIn, redis_client: Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):

    db_original_link_result = await db.execute(select(models.Link).filter(models.Link.original_link == link_data.original_link, models.Link.owner_id == current_user.id))
    db_original_link = db_original_link_result.scalar_one_or_none()

    if db_original_link:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У вас уже есть такая ссылка!'
        )
    
    short_code = get_short_code()

    existing_code_result = await db.execute(select(models.Link).where(models.Link.short_code == short_code))

    existing_code = existing_code_result.scalar_one_or_none()

    while existing_code:
        short_code = get_short_code()
        existing_code_result = await db.execute(select(models.Link).where(models.Link.short_code == short_code))
        existing_code = existing_code_result.scalar_one_or_none()

    new_link = models.Link(
        original_link=link_data.original_link,
        short_code=short_code,
        owner_id=current_user.id
    )

    db.add(new_link)
    await db.commit()

    await redis_client.delete(current_user.id)

    return new_link



@router.get('/links', response_model=list[schemas.LinkOut], status_code=status.HTTP_200_OK)
async def get_links(db: AsyncSession = Depends(get_db), redis_client: Redis = Depends(get_redis_client), current_user = Depends(get_current_user)):

    cache_key = current_user.id

    cache_links = await redis_client.get(cache_key)

    if cache_links:
        print(f'CACHE HIT to ID №{current_user.id}')

        return json.loads(cache_links)
    
    print('CACHE MISS')

    db_links_result = await db.execute(select(models.Link).where(models.Link.owner_id == current_user.id))

    db_links = db_links_result.scalars().all()

    if not db_links:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас пока нет ни одной ссылки, создайте новую!'
        )
    
    pydantic_links = [schemas.LinkOut.model_validate(lk) for lk in db_links]
    
    lk_to_redis = [lk.model_dump_json() for lk in pydantic_links]

    final_string = f"[{','.join(lk_to_redis)}]"
    await redis_client.set(cache_key, final_string, ex=600)
    
    return pydantic_links



@router.put('/links/{link_id}', response_model=schemas.LinkOut, status_code=status.HTTP_200_OK)
async def update_link(link_id: int, update_data: schemas.LinkIn, redis_client: Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):

    db_link_result = await db.execute(select(models.Link).where(models.Link.id == link_id))

    db_link = db_link_result.scalar_one_or_none()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет ссылки с таким id!'
        )
    
    if not db_link.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Ссылка с таким id не ваша! Вы не можете ее редактировать!'
        )
    
    update_link = update_data.model_dump(exclude_unset=True)

    for key, value in update_link.items():
        setattr(db_link, key, value)

    await db.commit()

    await db.refresh(db_link)

    await redis_client.delete(current_user.id)

    return db_link



@router.delete('/links/{link_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(link_id: int, redis_client: Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):

    db_link_result = await db.execute(select(models.Link).where(models.Link.id == link_id))

    db_link = db_link_result.scalar_one_or_none()

    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет ссылки с таким id!'
        )
    if not db_link.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Это не ваша ссылка, вы не можете ее удалить!'
        )
    
    await db.delete(db_link)
    await db.commit()

    await redis_client.delete(current_user.id)