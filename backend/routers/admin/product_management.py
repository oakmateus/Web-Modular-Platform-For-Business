from fastapi import APIRouter, HTTPException, status

from dependencies import SessionDep, AccessTokenDep
from ...database.models import CommercialType, CommercialItems, Promotions

from ...schemas import admin_schemas

from datetime import datetime, UTC

from enum import IntEnum

router = APIRouter(prefix="/admin", tags=["Products management"])

# ----- ITEMS CATEGORY MANAGEMENT -----

# Add products category

@router.post("/category")
def comercial_type(db: SessionDep, data: admin_schemas.CommercialType, token: AccessTokenDep):

    existing = db.query(CommercialType).filter(CommercialType.type_name == data.type_name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Categoria já existente.")

    new_category = CommercialType(**data.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# Exclude products category

@router.post("/category/delete")
def delete_comercial_type(db: SessionDep, data: admin_schemas.CommercialType, token: AccessTokenDep):

    category = db.get(CommercialType, data.type_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A categoria não existe.")

    db.delete(category)
    db.commit()

    return {"message": "Categoria excluida."}

# Change category name

@router.post("/category/update")
def update_comercial_type(db: SessionDep, data: admin_schemas.CommercialType, token: AccessTokenDep):

    category = db.query(CommercialType).filter(CommercialType.type_id == data.type_id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A categoria não existe.")

    category.update({"type_name": data.type_name})
    db.commit()

    return {"message": "Nome da categoria alterado."}

# ----- COMERCIAL ITEMS MANAGEMENT -----

# Add items to a category

@router.post("/items")
def comercial_items(db: SessionDep, data: admin_schemas.CommercialItems, token: AccessTokenDep):

    # Search for an existing category

    categories = db.query(CommercialType).first()

    if not categories:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Adicione uma categoria antes de adicionar um item ao catálogo.")

    # Verifying if the selected category already exist

    selected_category = db.get(CommercialType, data.type_id)

    if not selected_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A categoria não existe.")

    # Adding the new product to the database

    new_product = CommercialItems(**data.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product, {"message": "Novo produto adicionado."}

# Exclude comercial item

@router.post("/items/delete")
def delete_comercial_item(db: SessionDep, data: admin_schemas.CommercialItems, token: AccessTokenDep):

    item = db.get(CommercialItems, data.type_id)

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="O item não existe.")

    db.delete(item)
    db.commit()

    return {"message": "Item excluido."}

# Moving items to another category

@router.post("/items/update-category")
def update_item_category(db: SessionDep, data: admin_schemas.CommercialItems, token: AccessTokenDep):

    # Search for the item id on the table

    item = db.query(CommercialItems).filter(CommercialItems.item_id == data.item_id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="O item não existe.")

    # Verifying if the selected category already exist

    selected_category = db.get(CommercialType, data.type_id)
    
    if not selected_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A categoria não existe.")

    # Verifying if the selected item is already on the selected category

    if item.type_id == data.type_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="O item já pertence a esta categoria.")

    item.update({"type_id": data.type_id})
    db.commit()

    return {"message": "Produto alterado de categoria."}

# Update items information

# Declaring update options

class Options(IntEnum):
    NAME = 1 # Item name
    PRICE = 2 # Unity price
    QUANTITY = 3 # Quantity in stock
    IMAGE = 4 # Image url

@router.post("/items/update")
def update_item(db: SessionDep, operation: Options, data: admin_schemas.UpdateItems, token: AccessTokenDep):

    # Search for the item on the table
    
    item = db.query(CommercialItems).filter(CommercialItems.item_id == data.item_id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="O item não existe.")

    # Update item name

    if operation == Options.NAME:

        if item.item_name == data.item_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O nome não pode ser o mesmo.")

        item.update({"item_name": data.item_name})

    # Update uniti price

    elif operation == Options.PRICE:

        if item.unit_price == data.unit_price:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O preço não pode ser o mesmo.")

        item.update({"unit_price": data.unit_price})

    # Update quantity in stock

    elif operation == Options.QUANTITY:

        if item.quantity_in_stock == data.quantity_in_stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="A quantidade em estoque não pode ser a mesma.")

        item.update({"quantity_in_stock": data.quantity_in_stock})

    # Update image url

    elif operation == Options.IMAGE:

        if item.image_url == data.image_url:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="A url da imagem não pode ser a mesma.")

        item.update({"image_url": data.image_url})

    db.commit()

    return {"message": "Alteração salva."}

# ----- PROMOTIONS MANAGEMENT -----

# Creating a new promotion

@router.post("/promotions/creating")
def creating_promotions(db: SessionDep, data: admin_schemas.CreatingPromotions, token: AccessTokenDep):

    # Search for an existing item

    items = db.query(CommercialItems).first()

    if not items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Adicione um item antes de criar uma promoção.")

    # Verify if the promotion already exist

    promo_description = db.get(Promotions, data.promo_description)

    if promo_description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Esta promoção já existe.")

    # Verify if the expiration is out the date

    if data.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Esta data não pode ser utilizada para expiração.")

    new_promotion = Promotions(**data.dict())
    db.commit()
    db.refresh(new_promotion)

    return new_promotion, {"message": "A promoção foi criada."}

# Adding the promotion to an item

@router.post("/promotions/adding")
def adding_promotion(db: SessionDep, data: admin_schemas.AddingPromotion, token: AccessTokenDep):

    # Search for the promotion on the table
    
    promo = db.query(Promotions).filter(Promotions.promotional_id == data.promotional_id).first()

    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A promoção não existe.")

    # Verify if the expiration is out the date

    if promo.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Esta promoção está expirada.")

    # Verify if the promotion is active

    if promo.is_active == False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Esta promoção está inativa.")

    # Search for the item on the table

    items = []
    
    for item_id in data.item_id:

        current = db.query(CommercialItems).filter(CommercialItems.item_id == item_id).first()

        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"O item {item_id} não existe.")

        items.append(current)

    # Verify if the promotional price is valid
        
    for item in items:
        if promo.promotional_price >= item.unit_price:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O preço da promoção não pode ser igual ou superior ao valor padrão.")

    # Addint promotion to the selected product

    for item in items:
        item.update(CommercialItems({"promotional_id": data.promotional_id}))

    db.commit()

    return {"message": "Promoção adicionada ao produto."}
