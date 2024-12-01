from typing import Annotated
from fastapi import Depends, HTTPException

from config.db_adapter import DBSession

from sqlmodel import select

from models.entities.product import Product
from models.schemas.product import ProductCreate, ProductRead

class ProductService:
  def __init__(self, db: DBSession) -> None:
    self.db = db
  
  def get_all_products(self):
    products = self.db.exec(select(Product)).all() or []
    return products
  
  def get_product_by_id(self, id: int):
    product = self.db.get(Product, id)
    
    if product == None:
      raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead(id=product.id, name=product.name, price=product.price)

  def new_product(self, product: ProductCreate):
    new_product = Product(name=product.name, price=product.price)
    # Agrega un nuevo producto a la base de datos
    self.db.add(new_product)
    # Realiza los cambios en la base de datos
    self.db.commit()
    # Realiza los cambios en el objeto (Referencia al producto de la BD, así obtiene el nuevo ID)
    self.db.refresh(new_product)
    return ProductRead(id=new_product.id, name=new_product.name, price=new_product.price)

  def update_product(self, id: int, product: ProductCreate):
    product_db = self.db.get(Product, id)

    if product_db == None:
      raise HTTPException(status_code=404, detail="Product not found")
    
    product_db.name = product.name
    product_db.price = product.price
    self.db.add(product_db)
    self.db.commit()
    self.db.refresh(product_db)
    return ProductRead(id=product_db.id, name=product_db.name, price=product_db.price)

  def delete_product(self, id: int):
    product = self.db.get(Product, id)
    
    if product == None:
      raise HTTPException(status_code=404, detail="Product not found")
    
    self.db.delete(product)
    self.db.commit()
    return {"message": "Product deleted", "status": "success"}
  
SProductDependency = Annotated[ProductService, Depends(ProductService)]
    