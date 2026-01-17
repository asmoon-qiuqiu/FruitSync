from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session, select
from config import ACCESS_TOKEN_EXPIRE_HOURS
from schemas.user.userLogin import UserLogin, LoginResponse
from schemas.user.userResponse import UserResponse
from utils.hashPassword import verify_password
from utils.token import create_access_token
from model.user import User
from database import get_session
from datetime import timedelta, datetime
import logging  # 导入日志模块

# 配置日志（与注册接口保持一致，使用uvicorn日志器）
logger = logging.getLogger("uvicorn")
# 创建路由器
router = APIRouter(prefix="/api", tags=["login"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="用户登录接口",
    description="""
    #### 接口功能
    - 提供用户登录验证服务，支持通过用户名或邮箱作为账号进行登录
    - 验证通过后返回用户基本信息和临时身份令牌（JWT）
    #### 校验规则
    1. 账号校验：用户名/邮箱是否存在
    2. 密码校验：密码哈希比对（bcrypt算法）
    3. 状态校验：账户是否处于激活状态
    """,
)
async def login(
    login_data: UserLogin, session: Annotated[Session, Depends(get_session)]
):
    try:
        # 新增：记录登录请求开始（脱敏处理，密码不打印）
        logger.info(
            f"用户登录请求：登录账号={login_data.username}，请求时间={datetime.now()}"
        )

        # 查找用户(支持用户名或邮箱登录)
        statement = select(User).where(
            (User.username == login_data.username) | (User.email == login_data.username)
        )
        user = (await session.exec(statement)).first()

        # 1. 账号不存在校验
        if not user:
            logger.warning(f"登录失败：账号不存在，请求账号={login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
            )

        # 2. 密码错误校验
        if not verify_password(login_data.password, user.hashed_password):
            logger.warning(
                f"登录失败：密码错误，用户ID={user.id}，用户名={user.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
            )

        # 3. 账户禁用校验
        if not user.is_active:
            logger.warning(
                f"登录失败：账户已禁用，用户ID={user.id}，用户名={user.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="账户已被禁用"
            )

        # 生成JWT token
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        token = create_access_token(
            data={"sub": user.id, "username": user.username},
            expires_delta=access_token_expires,
        )

        # 新增：记录登录成功日志（包含用户关键信息，便于审计）
        logger.info(
            f"登录成功：用户ID={user.id}，用户名={user.username}，邮箱={user.email}，Token有效期={ACCESS_TOKEN_EXPIRE_HOURS}小时"
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

    # 新增：异常分类捕获与日志记录
    except HTTPException:
        # 业务异常（账号不存在/密码错误/账户禁用），直接抛出（已记录对应warning日志）
        raise
    except Exception as e:
        # 未知异常（数据库错误/Token生成失败等），记录错误日志并返回通用提示
        logger.error(
            f"登录失败：未知异常，请求账号={login_data.username}，异常详情={str(e)}",
            exc_info=True,  # 新增：打印完整堆栈信息，便于排查问题
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试",
        )
