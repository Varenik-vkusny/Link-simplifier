from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from ..database import get_db
from .. import models, schemas, security


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/register', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserIn, db: AsyncSession=Depends(get_db)):

    db_user_result = await db.execute(select(models.User).where(models.User.username == user.username))
    db_user = db_user_result.scalar_one_or_none()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким именем уже есть!'
        )
    
    password_hash = security.hash_password(user.password)

    db_user = models.User(**user.model_dump(), password_hash=password_hash)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user



@router.post('/token', response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def auth(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):

    db_user_result = await db.execute(select(models.User).where(models.User.username == user.username))
    
    db_user = db_user_result.scalar_one_or_none()

    authorization_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неправильное имя или пароль!'
    )

    if not db_user:
        raise authorization_exception
    if not security.verify_password(user.password, db_user.password_hash):
        raise authorization_exception
    

    user_data = {'sub': user.username}

    access_token = security.create_access_token(data=user_data)

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }



async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не авторизованы!'
    )

    try:
        payload = jwt.decode(token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM])

        username: str = payload.get('sub')

        if not username: 
            raise credential_exception
        
        token_data = schemas.TokenData(username)
    except JWTError: 
        raise credential_exception
    
    db_user_result = await db.execute(select(models.User).where(models.User.username == token_data.username))

    db_user = db_user_result.scalar_one_or_none()

    if not db_user:
        raise credential_exception
    
    return db_user