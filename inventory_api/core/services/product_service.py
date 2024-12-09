from typing import Annotated
from fastapi import Depends, HTTPException

from config.db_adapter import DBSession

from sqlmodel import select

from models.schemas.plant import PlantCreate
from models.entities.product import Product
from models.entities.supply import Supply
from models.schemas.product import ProductCreate, ProductRead, ProductUpdate

class ProductService:
  def __init__(self, db: DBSession) -> None:
    self.db = db
  
  def get_all(self):
    products_db = self.db.exec(select(Product)).all() or []
    return products_db
  
  async def get_all_supplies(self):
    products_db = self.db.exec(select(Product, Supply).join(Supply)).all()
    
    # List Comprehesion
    products = [ProductRead.supply_and_product(product, supply) for product, supply in products_db]
    
    products_sup = []
    for product, supply in products_db:
      products_sup.append(ProductRead.supply_and_product(product, supply))
    # products = [{"product": product, "supply": supply } for product, supply in products_db]
    return products_sup
  
  def get_by_id(self, id: int):
    product = self.db.get(Product, id)
    
    if product is None:
      raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead(**vars(product))

  def create(self, product: ProductCreate):
    product_db = Product.model_validate(product.model_dump())
    self.db.add(product_db)
    self.db.commit()
    self.db.refresh(product_db)
    
    product_read = ProductRead.model_validate(product_db)
    return product_read

  def update(self, id: int, product: ProductUpdate):
    product_db = self.db.get(Product, id)

    if product_db is None:
      raise HTTPException(status_code=404, detail="Product not found")
    
    # product_db.name = product.name
    # product_db.price = product.price
    # product_db.description = product.description
    # product_db.stock = product.stock
    # product_db.stock_minimum = product.stock_minimum
    # product_db.location = product.location
    # product_db.date_entry = product.date_entry
    # product_db.date_update = product.date_update
    # product_db.state = product.state
    
    for attr, value in product.model_dump(exclude_unset=True).items():
      setattr(product_db, attr, value)

    self.db.add(product_db)
    self.db.commit()
    self.db.refresh(product_db)
    return ProductRead(
                        id=product_db.id,
                        **product.model_dump(exclude_unset=True)
                       )

  def delete(self, id: int):
    product = self.db.get(Product, id)
    
    if product is None:
      raise HTTPException(status_code=404, detail="Product not found")
    
    self.db.delete(product)
    self.db.commit()
    return {"message": "Product deleted", "status": "success"}
  
SProductDependency = Annotated[ProductService, Depends(ProductService)]
    