from schemas.user.userRegister import UserRegister
from schemas.user.userResponse import UserResponse
from model.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session, or_  # or_ 用于合并查询
from database import get_session
from utils.hashPassword import hash_password
from typing import Annotated
from pydantic import ValidationError  # 捕获Pydantic校验异常
import logging  # 日志记录

# 配置日志
logger = logging.getLogger("uvicorn")
# 创建路由器
router = APIRouter(prefix="/api", tags=["register"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册接口",
    description="""
    #### 接口功能
    - 提供用户注册服务，完成用户账号的创建
    - 校验规则：
      1. 用户名/邮箱唯一性校验
      2. 用户名/密码/邮箱格式由Pydantic模型(UserRegister)前置校验
      3. 密码加密存储（bcrypt算法）
    - 入参说明:
    - username: 3-10位，仅含字母、数字、下划线、中文
    - email: 合法邮箱格式
    - password: 至少6位字符
    - repassword: 需与password一致（仅校验，不存储）
    """,
)
async def register(
    user_data: UserRegister, session: Annotated[Session, Depends(get_session)]
):
    try:
        # ========== 1. 唯一性校验（优化：封装函数，结构化错误） ==========
        # 构造查询：同时校验用户名和邮箱是否存在
        statement = select(User).where(
            or_(User.username == user_data.username, User.email == user_data.email)
        )
        existing_user = (await session.exec(statement)).first()

        # 判断是否存在重复，并区分是用户名还是邮箱
        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"field": "username", "message": "用户名已被注册"},
                )
            else:  # 邮箱重复
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"field": "email", "message": "邮箱已被注册"},
                )

        # ========== 2. 安全处理：显式忽略repassword（仅用password加密） ==========
        # repassword仅用于前端+Pydantic校验一致性，后端无需存储
        logger.info(f"用户注册：用户名={user_data.username}，邮箱={user_data.email}")

        # ========== 3. 创建新用户（密码加密存储） ==========
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),  # 仅password加密
        )

        # ========== 4. 数据库操作（增加异常捕获） ==========
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # 刷新获取数据库生成的字段（如id）

        logger.info(f"用户注册成功：用户名={user_data.username}，用户ID={new_user.id}")
        return new_user

    # ========== 5. 异常处理（分类捕获，友好提示） ==========
    except HTTPException:
        # 业务异常（用户名/邮箱已存在），直接抛出
        raise
    except ValidationError as e:
        # Pydantic校验异常（兜底，理论上FastAPI已提前校验）
        logger.error(f"用户注册参数校验失败：{e.errors()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"code": 422, "message": "参数格式错误", "errors": e.errors()},
        )
    except Exception as e:
        # 未知异常（数据库错误、加密错误等），记录日志并返回通用提示
        logger.error(f"用户注册失败：未知异常，详情={str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试",
        )
