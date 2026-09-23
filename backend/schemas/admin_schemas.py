from sqlmodel import SQLModel, Field 
from pydantic import EmailStr
from uuid import UUID
from decimal import Decimal
from datetime import date

# Administration account inputs

class AdminAccount(SQLModel):
    email: EmailStr
    password: str
    password_confirm: str | None = None
    remember_me: bool | None = None

# Token data

class AccessTokenData(SQLModel):
    admin_id: int | None = None

class RefreshTokenData(SQLModel):
    admin_id: int | None = None
    jti: UUID | None = None

# Comercial type inputs

class CommercialType(SQLModel):
    type_name: str
    type_id: int | None = None

# Comercial items inputs

class CommercialItems(SQLModel):
    item_id: int | None = None
    item_name: str
    type_id: int
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)
    promotional_id: int | None = None
    quantity_in_stock: int
    image_url: int

class UpdateItems(SQLModel):
    item_id: int
    item_name: str | None = None
    unit_price: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    quantity_in_stock: int | None = None
    image_url: str | None = None

# Promotions inputs

class CreatingPromotions(SQLModel):
    promotional_price: Decimal = Field(max_digits=10, decimal_places=2)
    promo_description: str
    expires_at: date

class AddingPromotion(SQLModel):
    item_id: list[int]
    promotional_id: int