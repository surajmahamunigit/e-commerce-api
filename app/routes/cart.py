from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models import CartItem, Product, User, user
from app.schemas.cart import CartItemCreate, CartItemResponse, CartResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post(
    "/add", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    request: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates the new cart or updates quantity if already exists.

    Args:
        request: Contains product_id and quantity to be added to the cart.
        current_user : Logged-in user from JWT token

    Returns:
        CartItem with updated quantity.
    """

    #  Get the product
    product_id = request.product_id
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    # Use current user
    user_id = current_user.id

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )

    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = CartItem(
            user_id=user_id, product_id=product_id, quantity=request.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item


@router.get("/", response_model=CartResponse)
def view_cart(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Returns cart with all the items, and total price .
    """

    user_id = current_user.id

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    total_price = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if product:
            total_price += float(product.price) * item.quantity

    return {
        "items": cart_items,
        "total_items": len(cart_items),
        "total_price": total_price,
    }


@router.delete("/remove/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deletes the CartItem.

    Args:
        product_id : UUId,

    Returns:
        No Content (status-code = 204)
    """

    try:
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product ID format"
        )

    # Current user
    user_id = current_user.id

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_uuid)
        .first()
    )

    if cart_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart."
        )

    db.delete(cart_item)
    db.commit()
