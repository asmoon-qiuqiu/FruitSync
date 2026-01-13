"""
商品模块响应数据模型（Pydantic v2）
功能：定义商品信息的标准化响应结构与创建商品的请求结构，用于商品相关接口的入参校验和出参格式化
适用场景：商品创建、商品详情查询、商品列表分页查询等接口
设计原则：
    1. 响应模型仅对外返回商品公开信息，无敏感/冗余字段；
    2. 请求模型合理设置默认值，降低前端传参成本；
    3. 字段类型与数据库模型严格对齐，保证数据一致性；
依赖：Pydantic（数据模型基类）、datetime（时间类型）、typing（列表类型注解）
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List


class ProductResponse(BaseModel):
    """商品信息响应模型
    作为单个商品数据的对外输出模板，统一返回商品核心公开信息
    字段说明：
        id: 商品唯一标识（数据库自增主键）
        name: 商品名称（符合业务规范的商品命名，长度限制参考数据库定义）
        description: 商品描述（商品的详细介绍信息）
        price: 商品售价（单位：元，保留两位小数，范围0-999.99）
        image_url: 商品主图URL（CDN存储的商品图片地址，支持HTTP/HTTPS）
        category: 商品分类（如水果/家电/服饰，与业务分类体系一致）
        in_stock: 库存状态（True-有库存可售卖，False-无库存下架）
        created_at: 商品创建时间（数据库记录的创建时间，统一为UTC时间）
    补充：
        该模型会被ProductListResponse嵌套使用，也可单独用于商品详情接口响应
    """

    id: int
    name: str
    description: str | None
    price: float
    image_url: str | None
    category: str
    in_stock: bool
    created_at: datetime


class ProductListResponse(BaseModel):
    """商品列表响应模型（带分页）
    定义分页查询商品列表时的标准化响应结构，兼顾数据返回与分页导航需求
    字段说明：
        total: 总记录数（符合筛选条件的商品总数，用于计算分页总数）
        page: 当前页码（从1开始，与前端请求的页码参数一致）
        page_size: 每页数量（单次返回的商品条数，范围1-100）
        total_pages: 总页数（由total/page_size向上取整计算得出，用于前端分页控件渲染）
        products: 商品列表（当前页的商品数据，元素为ProductResponse模型）
    补充：
        该模型仅返回有库存（in_stock=True）的商品数据，筛选逻辑由接口层实现
    """

    total: int  # 总记录数
    page: int  # 当前页码
    page_size: int  # 每页数量
    total_pages: int  # 总页数
    products: List[ProductResponse]  # 商品列表


class ProductCreateRequest(BaseModel):
    """创建商品请求模型
    作为创建商品接口的入参校验模板，规范前端传入的商品数据格式
    字段说明：
        name: 商品名称（必填，长度限制参考数据库定义）
        description: 商品描述（必填，简要说明商品特性/规格）
        price: 商品售价（必填，单位：元，需≥0且≤999.99）
        image_url: 商品主图URL（必填，需为合法的URL格式）
        category: 商品分类（可选，默认值为"水果"，需符合业务分类体系）
        in_stock: 库存状态（可选，默认值为True，创建时默认上架）
    补充：
        该模型仅做入参格式校验，商品创建时间（created_at）由后端自动生成，无需前端传入
    """

    name: str
    description: str
    price: float
    image_url: str
    category: str = "水果"
    in_stock: bool = True
