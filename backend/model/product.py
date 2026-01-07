"""
商品核心数据模型（SQLModel）
功能：定义数据库中商品表的结构与字段约束，存储商品的核心信息
适用场景：商品展示、商品管理、购物车等所有涉及商品数据的业务模块
技术说明：基于SQLModel实现，融合Pydantic的数据校验能力与SQLAlchemy的ORM操作能力，实现"模型即表结构"，
         支持自动生成数据库表、数据校验、CRUD操作等全流程功能
依赖：SQLModel（ORM模型与数据校验）、datetime（时间字段类型）、Field（字段约束定义）
"""

from sqlmodel import SQLModel, Field
from datetime import datetime


class Product(SQLModel, table=True):
    """
    商品核心数据表模型（对应数据库表：products）
    存储商品的基础展示信息和状态数据，核心业务表之一
    表设计核心原则：
        1. 可检索性：商品名称、分类字段设置索引，提升商品搜索/筛选效率
        2. 数据合法性：价格字段设置非负约束，避免异常价格数据
        3. 状态管控：通过in_stock字段控制商品的库存状态，支撑下单逻辑
        4. 时间追踪：记录商品创建时间和更新时间，便于商品上下架审计和追溯
    """

    # 显式指定数据库表名，若不指定则SQLModel默认使用类名小写复数（products），此处显式定义保持一致性
    __tablename__ = "products"

    # 主键字段：自增ID，default=None表示由数据库自动生成主键值，作为商品的唯一标识
    id: int | None = Field(default=None, primary_key=True)
    # 商品名称：普通索引（index=True），最大长度50，作为商品核心标识，提升检索效率；
    # 长度限制避免名称过长导致存储/展示异常，索引支撑商品名称模糊搜索、精准查询场景
    name: str = Field(max_length=50, index=True)
    # 商品描述：最大长度100，简要说明商品卖点和特性，支撑商品列表/详情页展示场景；
    # 长度限制平衡信息完整性与存储效率，避免冗余大文本数据
    description: str = Field(max_length=100)
    # 商品价格：ge=0（价格非负）、le=999.99（价格上限），存储商品售卖单价（单位：元/斤）；
    # 数值约束保障价格数据合法性，防止负价、超高价等异常数据入库，适配零售场景价格范围
    price: float = Field(ge=0, le=999.99)
    # 商品图片URL：最大长度500，存储商品展示图片的访问链接（支持CDN/OSS等存储方式的长链接）；
    # 长度适配各类云存储URL格式，保障图片链接完整存储
    image_url: str = Field(max_length=500)
    # 商品分类：默认值为"水果"，最大长度50，标识商品所属类别（如水果/蔬菜/零食）；
    # 索引设计支撑分类筛选、分类统计等业务场景，默认值降低新增商品的传参成本
    category: str = Field(default="水果", max_length=50, index=True)
    # 库存状态：默认值为True（有库存），通过此字段标记商品是否可售卖；
    # 下单逻辑需校验该字段，True时允许下单，False时商品下架/不可购，支撑库存管控
    in_stock: bool = Field(default=True)
    # 创建时间：默认使用当前时间（default_factory=datetime.now动态生成），记录商品上架时间；
    # 无需手动传入，由数据库层自动生成，便于商品上架时间排序、新品筛选等场景
    created_at: datetime = Field(default_factory=datetime.now)
    # 更新时间：默认使用当前时间，后续可通过业务逻辑（如商品编辑）更新；
    # 记录商品信息最后修改时间，便于数据审计、更新日志追溯、价格变动追踪等场景
    updated_at: datetime = Field(default_factory=datetime.now)
