from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session, select
from config import ACCESS_TOKEN_EXPIRE_HOURS
from schemas.userLogin import UserLogin, LoginResponse
from schemas.userResponse import UserResponse
from utils.hashPassword import verify_password
from utils.token import create_access_token
from model.user import User
from database import get_session
from datetime import timedelta


router = APIRouter(prefix="/api", tags=["login"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="用户登录接口",
    description="""
    #### 接口功能-提供用户登录验证服务，支持通过用户名或邮箱作为账号进行登录，验证通过后返回用户基本信息和临时身份令牌。
    """,
)
async def login(
    login_data: UserLogin, session: Annotated[Session, Depends(get_session)]
):
    # ""用户登录""
    # 查找用户(支持用户名或邮箱登录)
    statement = select(User).where(
        (User.username == login_data.username) | (User.email == login_data.username)
    )
    user = (await session.exec(statement)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用"
        )
    # 生成JWT token
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    token = create_access_token(
        data={"sub": user.id, "username": user.username},
        expires_delta=access_token_expires,
    )
    return LoginResponse(
        message="登录成功",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
        ),
        token=token,
    )
