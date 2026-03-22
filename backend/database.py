# 导入SQLAlchemy异步引擎创建函数（核心依赖）
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# 导入SQLModel异步会话类（SQLModel对SQLAlchemy AsyncSession的封装）
from sqlmodel.ext.asyncio.session import AsyncSession

# 导入项目配置（数据库连接信息、连接池参数等）
from config import settings

# 导入Python标准日志模块（用于记录数据库错误）
import logging

# 初始化日志器（logger名称为当前模块名，便于日志溯源）
logger = logging.getLogger(__name__)

# ==================== 异步数据库引擎配置 ====================
# 创建异步数据库引擎（SQLAlchemy核心组件，管理数据库连接池）
async_engine = create_async_engine(
    # 数据库连接URL（从配置文件读取，区分开发/生产环境）
    settings.DATABASE_URL,
    # 是否打印SQL语句：开发环境True（便于调试），生产环境False（减少日志）
    echo=settings.DB_ECHO,
    # 连接池常驻连接数：根据业务并发量配置，默认5
    pool_size=settings.DB_POOL_SIZE,
    # 连接池最大溢出连接数：超出pool_size的临时连接数，默认10
    max_overflow=settings.DB_MAX_OVERFLOW,
    # 连接池预检测：每次获取连接前执行ping，防止使用失效连接（生产环境必备）
    pool_pre_ping=True,
    # 连接回收时间：超过3600秒（1小时）自动回收连接，避免长期占用
    pool_recycle=3600,
)

# 创建异步会话工厂（SQLAlchemy核心组件，生成会话对象）
# 作用：封装会话创建规则，所有会话都通过该工厂生成，保证一致性
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,          # 绑定上面创建的异步引擎
    class_=AsyncSession,        # 指定会话类为SQLModel的AsyncSession（兼容SQLAlchemy）
    expire_on_commit=False,     # 提交后不自动过期实例（避免重复查询，生产环境推荐）
    autoflush=False,            # 关闭自动刷新（按需手动flush，更可控）
)

# ==================== 异步数据库会话依赖 ====================
async def get_session():
    """
    FastAPI异步数据库会话依赖项（核心函数）
    作用：为接口/业务函数提供独立的数据库会话，自动管理会话生命周期
    特性：异常自动回滚、错误日志记录、会话自动关闭
    """
    # 创建异步会话（async with 上下文管理器：自动管理会话的创建/关闭）
    
    # 从工厂创建会话
    session = AsyncSessionFactory()
    try:
        # 生成会话对象给依赖该函数的接口/业务函数使用
        # yield特性：函数执行到此处暂停，会话被外部使用；外部调用完成后，继续执行后续代码
        yield session

    except Exception as e:
        # 捕获会话使用过程中所有异常（如SQL执行错误、连接异常等）
        # exc_info=True：记录完整异常堆栈，便于定位错误代码行
        logger.error(f"数据库会话执行异常：{str(e)}", exc_info=True)
        # 异常时回滚事务：避免未提交的脏数据残留，保证数据一致性
        await session.rollback()
        # 重新抛出异常：让FastAPI捕获并返回500错误给前端，不吞异常
        raise

    finally:
        # 最终块：无论是否发生异常，都会执行，确保会话被正确关闭，释放数据库连接回连接池
        # 防止极端场景下（如async with内部异常）会话未正常关闭导致连接池耗尽
        await session.close()


# ==================== 注意事项 ====================
# 1. 同步引擎/会话兼容：
#    若项目仍有同步代码，需保留 from sqlmodel import create_engine, Session
#    纯异步场景下可删除同步相关导入
# 2. 会话关闭机制：
#    async with 上下文管理器会在退出时自动调用session.close()
#    finally块中的手动close是生产环境的兜底保障，非多余操作
# 3. 连接池参数调优：
#    pool_pre_ping/pool_recycle 是生产环境必备参数，防止数据库连接失效
#    pool_size/max_overflow 需根据业务QPS调整，避免连接数过多/过少
