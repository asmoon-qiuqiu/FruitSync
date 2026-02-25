"""
邮箱验证码密码重置API路由
功能：提供基于邮箱验证码的密码重置完整流程接口
流程：发送验证码 → 验证验证码 → 重置密码（三步走）
依赖：FastAPI（路由框架）、SQLModel（数据库操作）、JWT（令牌生成）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select