import stripe
from app.config import get_settings

settings = get_settings()

# Initialize Stripe with secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount: float, currency: str = "usd") -> dict:
    """
    Creates a Strip PaymentInent.

    Args:
        amount: Total amount in dollars
        currency: Currency code (default: usd)

    Returns:
        dict with client_secret and payment_intent_id
    """

    # Convert dollars to cents (for Strip)
    amount_in_cents = int(amount * 100)

    payment_intent = stripe.PaymentIntent.create(
        amount=amount_in_cents,
        currency=currency,
        payment_method_types=["card"],
    )

    return {
        "client_secret": payment_intent.client_secret,
        "payment_intent_id": payment_intent.id,
    }
