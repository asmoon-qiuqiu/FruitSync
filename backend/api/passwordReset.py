"""
邮箱验证码密码重置API路由
功能：提供基于邮箱验证码的密码重置完整流程接口
流程：发送验证码 → 验证验证码 → 重置密码（三步走）
依赖：FastAPI（路由框架）、SQLModel（数据库操作）、JWT（令牌生成）
"""

from ast import expr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session, update
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import random
import logging

from model.user import User
from model.verificationCode import VerificationCode
from schemas.email.email import (
    SendCodeRequest,
    VerifyCodeRequest,
    ResetPasswordRequest,
)
from database import get_session
from utils.hashPassword import hash_password
from utils.emailService import email_service
from utils.token import create_reset_token
from config import settings
import jwt

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/password", tags=["password-reset"])


def generate_verification_code() -> str:
    """生成6位随机数字验证码"""
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


@router.post(
    "/send-code",
    status_code=status.HTTP_200_OK,
    summary="发送密码重置验证码",
    description="""
    #### 接口功能
    - 向用户注册邮箱发送6位数字验证码
    - 验证码有效期5分钟
    - 同一邮箱60秒内只能发送一次验证码（防止恶意刷验证码）
    
    #### 校验规则
    1. 邮箱格式校验（Pydantic自动完成）
    2. 邮箱是否已注册
    3. 发送频率限制（60秒内不可重复发送）
    """,
)
async def send_verification_code(
    request: SendCodeRequest, session: Session = Depends(get_session)
):
    """发送密码重置验证码"""
    try:
        # 1. 校验邮箱是否已注册
        statement = select(User).where(User.email == request.email)
        user = (await session.exec(statement)).first()

        if not user:
            # 为了安全，即使邮箱不存在也返回成功消息（防止邮箱枚举攻击）
            logger.warning(f"发送验证码失败：邮箱未注册，邮箱={request.email}")
            return {"message": "如果该邮箱已注册，验证码将发送到您的邮箱"}

        # 2. 防刷校验：检查60秒内是否已发送验证码
        one_minute_ago = datetime.now(ZoneInfo("Asia/Shanghai")) - timedelta(seconds=60)
        recent_code_statement = (
            select(VerificationCode)
            .where(
                VerificationCode.email == request.email,
                VerificationCode.created_at >= one_minute_ago,
                VerificationCode.code_type == "password_reset",
            )
            .order_by(VerificationCode.created_at.desc())
        )
        recent_code = (await session.exec(recent_code_statement)).first()

        if recent_code:
            created_at = recent_code.created_at

            # 统一时区，不再报时区错误
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=ZoneInfo("Asia/Shanghai"))

            remaining_seconds = 60 - int(
                (datetime.now(ZoneInfo("Asia/Shanghai")) - created_at).total_seconds()
            )

            if remaining_seconds > 0:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"验证码发送过于频繁，请{remaining_seconds}秒后再试",
                )
        # 3. 生成6位数字验证码
        code = generate_verification_code()

        # 4. 计算验证码过期时间（5分钟）
        expires_at = datetime.now(ZoneInfo("Asia/Shanghai")) + timedelta(
            minutes=settings.VERIFY_CODE_EXPIRE_MINUTES
        )

        # 5. 保存验证码到数据库
        verification = VerificationCode(
            email=request.email,
            code=code,
            expires_at=expires_at,
            code_type="password_reset",
        )
        session.add(verification)

        # 6. 发送验证码邮件
        email_sent = email_service.send_verification_code(request.email, code)

        if not email_sent:
            # 邮件发送失败，回滚数据库操作
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="验证码邮件发送失败，请稍后重试",
            )
        await session.commit()

        logger.info(
            f"验证码发送成功：邮箱={request.email}，验证码={code}（仅开发环境日志）"
        )

        return {
            "message": "验证码已发送到您的邮箱，请查收",
            "expires_in": settings.VERIFY_CODE_EXPIRE_MINUTES * 60,  # 秒数
            # 开发环境返回验证码（生产环境删除）
            "debug_code": code if settings.is_development else None,
        }

    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        logger.error(
            f"发送验证码失败：邮箱={request.email}，错误={str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试",
        )


@router.post(
    "/verify-code",
    status_code=status.HTTP_200_OK,
    summary="验证验证码有效性",
    description="""
    #### 接口功能
    - 验证用户输入的验证码是否正确且未过期
    - 验证通过后返回重置密码令牌（JWT）
    
    #### 校验规则
    1. 验证码格式校验（6位数字）
    2. 验证码是否存在
    3. 验证码是否已使用
    4. 验证码是否过期
    """,
)
async def verify_code(
    request: VerifyCodeRequest, session: Session = Depends(get_session)
):
    """验证验证码"""
    try:
        # 1. 格式校验：验证码必须是6位数字
        if not request.code.isdigit() or len(request.code) != 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码格式错误，必须是6位数字",
            )

        # 2. 查询验证码记录
        statement = (
            select(VerificationCode)
            .where(
                VerificationCode.email == request.email,
                VerificationCode.code == request.code,
                VerificationCode.code_type == "password_reset",
                VerificationCode.is_used == False,
                VerificationCode.expires_at
                >= datetime.now(ZoneInfo("Asia/Shanghai")),  # 只查未过期的
            )
            .with_for_update()
        )
        verification = (await session.exec(statement)).first()

        if not verification:
            logger.warning(
                f"验证码验证失败：验证码不存在或已使用，邮箱={request.email}，验证码={request.code}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误或已失效"
            )

        # 3. 验证码过期校验
        now = datetime.now(ZoneInfo("Asia/Shanghai"))
        expires_at = verification.expires_at
        # 如果数据库取出的expires_at没有时区信息，默认设置为上海时区
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=ZoneInfo("Asia/Shanghai"))

        if now > expires_at:
            logger.warning(
                f"验证码验证失败：验证码已过期，邮箱={request.email}，验证码={request.code}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码已过期，请重新获取",
            )

        # 4. 标记验证码为已使用
        update_stmt = (
            update(VerificationCode)
            .where(
                VerificationCode.id == verification.id,
                VerificationCode.is_used == False,  # 再次校验，防止并发修改
            )
            .values(is_used=True)
        )
        result = await session.exec(update_stmt)
        await session.commit()
        if result.rowcount == 0:
            logger.warning(
                f"验证码验证失败：验证码已被其他请求使用，邮箱={request.email}，验证码={request.code}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="验证码已失效"
            )

        # 5. 生成重置密码令牌（JWT，有效期5分钟）
        reset_token = create_reset_token({"email": request.email, "type": "reset"})

        logger.info(f"验证码验证成功：邮箱={request.email}")

        return {
            "message": "验证码验证成功",
            "reset_token": reset_token,
            "expires_in": settings.RESET_TOKEN_EXPIRE_MINUTES * 60,  # 秒数
        }

    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        logger.error(
            f"验证验证码失败：邮箱={request.email}，错误={str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试",
        )


@router.post(
    "/reset",
    status_code=status.HTTP_200_OK,
    summary="重置密码",
    description="""
    #### 接口功能
    - 使用重置令牌重置用户密码
    - 密码重置成功后发送通知邮件
    
    #### 校验规则
    1. 重置令牌有效性校验（JWT解析）
    2. 令牌是否过期
    3. 新密码格式校验（至少6位字符）
    """,
)
async def reset_password(
    request: ResetPasswordRequest, session: Session = Depends(get_session)
):
    """重置密码"""
    try:
        # 1. 验证重置令牌
        try:
            payload = jwt.decode(
                request.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email = payload.get("email")
            token_type = payload.get("type")

            if not email or token_type != "reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="无效的重置令牌"
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="重置令牌已过期，请重新获取验证码",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="无效的重置令牌"
            )

        # 2. 新密码格式校验
        if len(request.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="密码长度至少6个字符"
            )

        # 3. 查询用户
        statement = select(User).where(User.email == email)
        user = (await session.exec(statement)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
            )

        # 4. 更新用户密码
        user.hashed_password = hash_password(request.new_password)
        user.updated_at = datetime.now(ZoneInfo("Asia/Shanghai"))

        user_id = user.id
        username = user.username

        session.add(user)
        await session.commit()

        # 5. 发送密码重置成功通知邮件（异步发送，失败不影响主流程）
        try:
            email_service.send_password_reset_success(email, username)
        except Exception as e:
            logger.warning(f"密码重置成功通知邮件发送失败：{str(e)}")

        logger.info(
            f"密码重置成功：用户ID={user_id}，用户名={username}，邮箱={email}"
        )

        return {"message": "密码重置成功，请使用新密码登录"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"密码重置失败：错误={str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试",
        )
