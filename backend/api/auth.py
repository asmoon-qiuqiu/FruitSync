# api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from datetime import datetime

from model.user import User
from model.password_reset import PasswordReset
from schemas.auth import (
    PasswordResetRequest,
    PasswordResetConfirm,
)

from database import get_session
from utils.hashPassword import hash_password
from utils.token import create_access_token, get_reset_expiration

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/forgot-password")
def forgot_password(
    reset_request: PasswordResetRequest, session: Session = Depends(get_session)
):
    # 忘记密码 - 发送重置链接
    # 查找用户
    statement = select(User).where(User.email == reset_request.email)
    user = session.exec(statement).first()

    if not user:
        # 为了安全,即使用户不存在也返回成功消息
        return {"message": "如果该邮箱已注册,重置链接已发送到您的邮箱"}

    token = create_access_token()
    expires_at = get_reset_expiration()

    reset_record = PasswordReset(user_id=user.id, token=token, expires_at=expires_at)

    session.add(reset_record)
    session.commit()
    # 实际应用中这里应该发送邮件
    reset_link = f"http://localhost:5173/reset-password?token={token}"
    print(f"密码重置链接: {reset_link}")

    return {
        "message": "如果该邮箱已注册,重置链接已发送到您的邮箱",
        "debug_token": token,  # 仅用于测试,生产环境删除
    }


@router.post("/reset-password")
def reset_password(
    reset_data: PasswordResetConfirm, session: Session = Depends(get_session)
):
    """重置密码"""
    # 查找重置令牌
    statement = select(PasswordReset).where(
        PasswordReset.token == reset_data.token, PasswordReset.is_used == False
    )
    reset_record = session.exec(statement).first()

    if not reset_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="无效的重置令牌"
        )

    if datetime.now() > reset_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="重置链接已过期"
        )
    # 更新用户密码
    statement = select(User).where(User.id == reset_record.user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    user.hashed_password = hash_password(reset_data.new_password)
    user.updated_at = datetime.now()
    # 标记令牌为已使用
    reset_record.is_used = True

    session.add(user)
    session.add(reset_record)
    session.commit()

    return {"message": "密码重置成功"}


@router.get("/verify-reset-token/{token}")
def verify_reset_token(token: str, session: Session = Depends(get_session)):
    #  """验证重置令牌是否有效"""
    statement = select(PasswordReset).where(
        PasswordReset.token == token, PasswordReset.is_used == False
    )
    reset_record = session.exec(statement).first()

    if not reset_record or datetime.now() > reset_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="无效或已过期的令牌"
        )

    return {"message": "令牌有效", "valid": True}
