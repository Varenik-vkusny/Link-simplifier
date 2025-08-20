import logging
from sqlalchemy import update
from .database import AsyncLocalSession
from .client import get_redis_client
from . import models


async def sync_redis_clicks_to_db():
    try:
        async with AsyncLocalSession() as db:

            redis_client = get_redis_client()

            click_keys = [key async for key in redis_client.scan_iter("clicks:*")]

            if not click_keys:

                logging.info('Не найдено ключей нажатий')
                return

            click_counts = await redis_client.mget(click_keys)

            updates = []
            keys_to_delete = []
            for key, count in zip(click_keys, click_counts):
                if count is not None:
                    short_code = key.split(':')[-1]
                    updates.append({
                        'short_code': short_code,
                        'increment_by': int(count)
                    })
                    keys_to_delete.append(key)


            if not updates:
                logging.info('Нечего обновлять')

                return
            

            updated_count = 0
            for u in updates:
                stmt = (
                    update(models.Link).where(models.Link.short_code == u['short_code']).values(click_count=models.Link.click_count + u['increment_by'])
                )
                await db.execute(stmt)
                updated_count += 1

            await db.commit()


            logging.info(f'Обновлено {updated_count} счетчиков')
        
        if keys_to_delete:
            await redis_client.delete(*keys_to_delete)

    except Exception as e:
        logging.info(f'Ошибка при сихронизации: {e}')
        await db.rollback()