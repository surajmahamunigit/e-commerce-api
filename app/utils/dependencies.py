from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import User
from app.utils.security import verify_access_token


def get_current_user(
    authorization: str = Header(None), db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token"""

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    token = authorization.split(" ")[1]

    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
