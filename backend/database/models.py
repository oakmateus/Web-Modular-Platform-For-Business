from datetime import datetime, date
from sqlmodel import Field, SQLModel, UUID
from decimal import Decimal
from pydantic import EmailStr

class CommercialType(SQLModel, table=True):
    type_id: int | None = Field(default=None, primary_key=True)
    type_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Promotions(SQLModel, table=True):
    promotional_id: int | None = Field(default=None, primary_key=True)
    promotional_price: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: date
    is_active: bool = Field(default=True)

class CommercialItems(SQLModel, table=True):
    item_id: int | None = Field(default=None, primary_key=True)
    item_name: str
    type_id: int = Field(foreign_key="commercialtype.type_id")
    unit_price: Decimal
    promotional_id: int | None = Field(default=None, foreign_key="promotions.promotional_id")
    quantity_in_stock: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    image_url: str

class Orders(SQLModel, table=True):
    order_id: int | None = Field(default=None, primary_key=True)
    client_name: str
    email: EmailStr
    subtotal: Decimal
    discount_total: Decimal
    delivery_fee: Decimal
    total_price: Decimal
    payment_method: str
    order_status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderItems(SQLModel, table=True):
    order_item_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    item_id: int = Field(foreign_key="commercialitems.item_id")
    quantity: int
    unit_price: Decimal

class OrderDelivery(SQLModel, table=True):
    delivery_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    provider: str
    external_order_id: int
    gross_value: Decimal
    dicount: Decimal
    net_value: Decimal
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Admin(SQLModel, table=True):
    admin_id: int = Field(default=1, primary_key=True, sa_column_kwargs={"check": "id = 1"})
    email: EmailStr = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminAccess(SQLModel, table=True):
    token_id: UUID | None = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.admin_id")
    is_revoked: bool
    accessed_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: date
    logout_at: date