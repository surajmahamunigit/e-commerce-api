from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.models import Order, OrderItem, CartItem, Product, User
from app.schemas.order import OrderResponse, OrderItemResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
def checkout(db: Session = Depends(get_db)):
    """
    Returns order details after successful checkout.
    """

    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user_id = user.id

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty."
        )

    # Create order with total price calculated from cart items
    total_amount = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total_amount += float(product.price) * item.quantity
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found.",
            )

    order = Order(user_id=user_id, total_amount=total_amount, status="pending")
    db.add(order)
    db.commit()
    db.refresh(order)

    # create order items to capture the price_at_purchase and subtotal for each item
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()

        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                subtotal=product.price * cart_item.quantity,
                price_at_purchase=product.price,
            )
            db.add(order_item)

    db.commit()

    # Clear the cart after checkout
    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()

    # Get all the order items to complete the order
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "stripe_payment_id": order.stripe_payment_id,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": order_items,
    }


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """
    Returns list of orders with items for the user
    """

    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not in database"
        )

    user_id = user.id

    # Get all orders for a user, and attach items to the orders
    orders = db.query(Order).filter(Order.user_id == user_id).all()

    result = []
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        result.append(
            {
                "id": order.id,
                "user_id": order.user_id,
                "total_amount": order.total_amount,
                "status": order.status,
                "stripe_payment_id": order.stripe_payment_id,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "items": order_items,
            }
        )

    return result


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    """
    Returns single order with order items
    """

    # Covert the string to UUId
    try:
        order_uuid = UUID(order_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order ID format"
        )

    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users in database. Register first.",
        )
    user_id = user.id

    order = db.query(Order).filter(Order.id == order_uuid).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    order.items = order_items

    return order
