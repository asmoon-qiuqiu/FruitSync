# main.py
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager  # 用于管理应用生命周期
from sqlmodel import SQLModel
from database import async_engine
from fastapi.staticfiles import StaticFiles
from api.register import router as register
from api.login import router as login
from api.product import router as product
from api.passwordReset import router as passwordReset
from config import settings  # 配置系统
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    try:
        # 启动逻辑
        logger.info(f"🚀 应用启动中... 环境: {settings.ENVIRONMENT.value}")
        logger.info(
            f"📊 数据库: {settings.DATABASE_URL.split('@')[-1]}"
        )  # 只打印主机信息

        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        logger.info("✅ 应用启动成功，数据库表已创建")

        # 开发环境显示更多信息
        if settings.is_development:
            logger.info(f"🔧 调试模式: {settings.DEBUG}")
            logger.info(f"🌐 CORS允许来源: {settings.CORS_ORIGINS}")
            logger.info(f"⏰ Token过期时间: {settings.ACCESS_TOKEN_EXPIRE_HOURS}小时")

    except Exception as e:
        logger.error(f"❌ 应用启动失败：{str(e)}")
        raise

    yield

    try:
        # 关闭逻辑
        logger.info("👋 应用正在关闭...")
        await async_engine.dispose()
        logger.info("✅ 应用已关闭，资源已清理")
    except Exception as e:
        logger.error(f"❌ 应用关闭失败：{str(e)}")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# 挂载静态文件目录
try:
    app.mount("/images", StaticFiles(directory=settings.STATIC_DIR), name="images")
except Exception as e:
    logger.warning(f"⚠️ 静态文件目录挂载失败: {e}")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由
app.include_router(register)
app.include_router(login)
app.include_router(product)
app.include_router(passwordReset)


# 全局捕获参数校验错误，统一返回格式
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 取出第一个错误
    error = exc.errors()[0]
    loc = error.get("loc", [])
    field = loc[-1]  # 获取字段名 page / page_size / username 等
    msg = error.get("msg", "参数格式错误")

    # 返回你要的格式！
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"field": field, "message": msg}},
    )


# 根路径
@app.get("/")
def root():
    return {
        "message": "🤓欢迎调用asmoon的API",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
        "endpoints": {
            "register": "/api/register",
            "login": "/api/login",
            "products": "/api/products",
            "forgot_password": "/api/auth/forgot-password",
            "reset_password": "/api/auth/reset-password",
        },
    }


# 健康检查端点
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT.value,
        "version": settings.APP_VERSION,
    }


# 启动命令
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,  # 开发环境自动重载
        log_level="info" if settings.is_development else "warning",
    )
