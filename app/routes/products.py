from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.utils.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """
    Returns the list of all products in the database.
    No authentication required here, as this is a public endpoint.
    """

    products = db.query(Product).all()

    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """
    Args:
    product_id: UUID of the product to retrieve.

    Returns:
    Single product or 404 error
    """

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """ "
    Requires Authentication.
    Only authenticated users can create the products.

    Args:
        product_data: ProductCreate schema contaning the data for the new product.
        current_user: Logged in user.

    Returns:
        Created product with product_id.
    """

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Requires authentication.

    Args:
        product_id : UUID,
        product_data: ProductUpdate,
        current_user: Logged in user.

    Returns:
        Updated product.
    """

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.description is not None:
        product.description = product_data.description

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.stock is not None:
        product.stock = product_data.stock

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Requires authentication.

    Args:
        product_id : UUID,
        current_user: Logged in user.

    Returns:
        No content, 204 status code (deleted ).
    """

    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return None
