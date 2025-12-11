from schemas.userRegister import UserRegister
from model.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.userResponse import UserResponse
from sqlmodel import select, Session
from database import get_session
from utils.hashPassword import hash_password
from typing import Annotated

router = APIRouter(prefix="/api", tags=["register"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册接口",
    description="""
    #### 接口功能-提供用户注册服务，完成用户账号的创建，注册时会对用户名和邮箱进行唯一性校验，同时将用户密码加密后存储，保障账户安全。
    """,
)
async def register(
    user_data: UserRegister, session: Annotated[Session, Depends(get_session)]
):
    # 构造查询语句：查询User表中username等于前端传递的用户名
    statement = select(User).where(User.username == user_data.username)
    # 执行查询并获取第一条结果（exec返回迭代器，first()取第一条）
    existing_user = (await session.exec(statement)).first()
    # 用户名已存在，抛出400错误（Bad Request）
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已被注册"
        )
    # 检查邮箱是否已存在
    statement = select(User).where(User.email == user_data.email)
    existing_email = (await session.exec(statement)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册"
        )
    # 创建新用户
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
