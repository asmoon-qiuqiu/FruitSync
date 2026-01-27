"""应用配置模块"""

from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Environment(str, Enum):
    """环境枚举"""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """应用配置类"""

    # ==================== 环境配置 ====================
    ENVIRONMENT: Environment = Field(
        default=Environment.DEVELOPMENT, description="运行环境"
    )

    # ==================== 数据库配置 ====================
    # 开发环境数据库
    DEV_DB_HOST: str = Field(default="localhost", description="开发数据库主机")
    DEV_DB_PORT: int = Field(default=3306, description="开发数据库端口")
    DEV_DB_USER: str = Field(default="root", description="开发数据库用户名")
    DEV_DB_PASSWORD: str = Field(default="23718", description="开发数据库密码")
    DEV_DB_NAME: str = Field(default="fruit_db", description="开发数据库名称")

    # 生产环境数据库
    PROD_DB_HOST: str = Field(default="", description="生产数据库主机")
    PROD_DB_PORT: int = Field(default=3306, description="生产数据库端口")
    PROD_DB_USER: str = Field(default="", description="生产数据库用户名")
    PROD_DB_PASSWORD: str = Field(default="", description="生产数据库密码")
    PROD_DB_NAME: str = Field(default="fruit_db_prod", description="生产数据库名称")

    # 数据库连接池配置
    DB_POOL_SIZE: int = Field(default=5, description="连接池大小")
    DB_MAX_OVERFLOW: int = Field(default=10, description="连接池最大溢出")
    DB_ECHO: bool = Field(default=False, description="是否打印SQL语句")

    # ==================== JWT配置 ====================
    # JWT核心配置项（基于Pydantic Field定义，用于配置校验和文档生成）
    # 核心密钥，生产环境必须配置高强度随机字符串（建议32位以上），切勿泄露
    SECRET_KEY: str = Field(default="", description="JWT密钥，生产环境必须设置")
    # JWT签名算法，HS256为对称加密算法，实现简单且性能高，适合中小型系统
    ALGORITHM: str = Field(default="HS256", description="JWT签名算法")
    # 访问令牌有效期，需平衡用户体验（有效期太短需频繁登录）和安全性（太长风险高）
    ACCESS_TOKEN_EXPIRE_HOURS: int = Field(
        default=6, description="访问令牌过期时间(小时)"
    )
    # 重置密码令牌有效期，敏感操作令牌建议设置短有效期，降低泄露风险
    RESET_TOKEN_EXPIRE_HOURS: int = Field(
        default=1, description="重置密码令牌过期时间(小时)"
    )
    # 验证码过期时间（分钟）
    # 短信/邮箱验证码等一次性验证场景使用，3-5分钟为行业通用合理时长
    VERIFY_CODE_EXPIRE_MINUTES: int = Field(
        default=5, description="验证码过期时间（分钟）"
    )

    # ==================== 应用配置 ====================
    APP_TITLE: str = Field(default="水果商城API", description="应用标题")
    APP_VERSION: str = Field(default="1.0.0", description="应用版本")
    DEBUG: bool = Field(default=True, description="调试模式")

    # ==================== CORS配置 ====================
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173"], description="允许的跨域来源"
    )

    # ==================== 服务器配置 ====================
    HOST: str = Field(default="0.0.0.0", description="服务器主机")
    PORT: int = Field(default=8000, description="服务器端口")

    # ==================== 静态文件配置 ====================
    STATIC_DIR: str = Field(default="static/images", description="静态文件目录")

    # ==================== 邮件配置（可选） ====================
    SMTP_HOST: str = Field(default="", description="SMTP服务器主机")
    SMTP_PORT: int = Field(default=587, description="SMTP服务器端口")
    SMTP_USER: str = Field(default="", description="SMTP用户名")
    SMTP_PASSWORD: str = Field(default="", description="SMTP密码")
    EMAIL_FROM: str = Field(default="", description="发件人邮箱")

    # ==================== Redis配置（可选） ====================
    REDIS_HOST: str = Field(default="localhost", description="Redis主机")
    REDIS_PORT: int = Field(default=6379, description="Redis端口")
    REDIS_PASSWORD: str = Field(default="", description="Redis密码")
    REDIS_DB: int = Field(default=0, description="Redis数据库编号")

    #  V1写法：用 model_config 替代 Config 类
    # class Config:
    #     # 从.env文件读取配置
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    #     case_sensitive = True

    #  V2 新写法：用 model_config 替代 Config 类
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # ==================== 动态属性 ====================
    @property
    def DATABASE_URL(self) -> str:
        """根据环境返回对应的数据库连接字符串"""
        if self.ENVIRONMENT == Environment.PRODUCTION:
            return (
                f"mysql+aiomysql://{self.PROD_DB_USER}:{self.PROD_DB_PASSWORD}"
                f"@{self.PROD_DB_HOST}:{self.PROD_DB_PORT}/{self.PROD_DB_NAME}"
            )
        else:
            return (
                f"mysql+aiomysql://{self.DEV_DB_USER}:{self.DEV_DB_PASSWORD}"
                f"@{self.DEV_DB_HOST}:{self.DEV_DB_PORT}/{self.DEV_DB_NAME}"
            )

    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.ENVIRONMENT == Environment.PRODUCTION

    def model_post_init(self, __context) -> None:
        """初始化后的验证"""
        # 生产环境必须设置SECRET_KEY
        if self.is_production and not self.SECRET_KEY:
            raise ValueError("生产环境必须设置SECRET_KEY")

        # 生产环境必须设置数据库配置
        if self.is_production:
            if not all([self.PROD_DB_HOST, self.PROD_DB_USER, self.PROD_DB_PASSWORD]):
                raise ValueError("生产环境必须配置完整的数据库信息")

        # 开发环境自动生成SECRET_KEY
        if self.is_development and not self.SECRET_KEY:
            import secrets

            self.SECRET_KEY = secrets.token_hex(32)
            print(f"⚠️ 开发环境自动生成SECRET_KEY: {self.SECRET_KEY}")


# 创建全局配置实例
settings = Settings()

# 向后兼容：导出常用配置
DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = settings.ACCESS_TOKEN_EXPIRE_HOURS
RESET_TOKEN_EXPIRE_HOURS = settings.RESET_TOKEN_EXPIRE_HOURS
