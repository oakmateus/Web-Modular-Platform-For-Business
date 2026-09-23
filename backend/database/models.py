from datetime import datetime, date
from sqlmodel import Field, SQLModel, CheckConstraint
from decimal import Decimal
from uuid import UUID

# Items categories table

class CommercialType(SQLModel, table=True):
    type_id: int | None = Field(default=None, primary_key=True)
    type_name: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Items promotions table

class Promotions(SQLModel, table=True):
    promotional_id: int | None = Field(default=None, primary_key=True)
    promotional_price: Decimal
    promo_description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: date
    is_active: bool = Field(default=True)

# Commercial items table

class CommercialItems(SQLModel, table=True):
    item_id: int | None = Field(default=None, primary_key=True)
    item_name: str
    type_id: int = Field(foreign_key="commercialtype.type_id", ondelete="CASCADE")
    unit_price: Decimal
    promotional_id: int | None = Field(default=None, foreign_key="promotions.promotional_id", ondelete="SET NULL")
    quantity_in_stock: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    image_url: str

# Clients orders table

class Orders(SQLModel, table=True):
    order_id: int | None = Field(default=None, primary_key=True)
    client_name: str
    email: str
    subtotal: Decimal
    discount_total: Decimal
    delivery_fee: Decimal
    total_price: Decimal
    payment_method: str
    order_status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Clients order items table

class OrderItems(SQLModel, table=True):
    order_item_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id", ondelete="CASCADE")
    item_id: int = Field(foreign_key="commercialitems.item_id", ondelete="CASCADE")
    quantity: int
    unit_price: Decimal

# Orders delivery informations table

class OrderDelivery(SQLModel, table=True):
    delivery_id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id", ondelete="CASCADE")
    provider: str
    external_order_id: int
    gross_value: Decimal
    dicount: Decimal
    net_value: Decimal
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Administration account table

class Admin(SQLModel, table=True):
    admin_id: int = Field(default=1, primary_key=True, sa_column_args={CheckConstraint("admin_id = 1")})
    email: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Administration access control table

class AdminAccess(SQLModel, table=True):
    token_id: UUID | None = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.admin_id", ondelete="CASCADE")
    is_revoked: bool
    accessed_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: date
    logout_at: date