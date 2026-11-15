import stripe
from django.conf import settings

# Устанавливаем ключ (можно также сделать это в settings.py)
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id: str, amount: int) -> str:
    """Создает цену в Stripe (в копейках) и возвращает ее ID."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # Переводим рубли в копейки
        currency="rub",
    )
    return price.id


def create_stripe_session(price_id: str) -> dict:
    """Создает сессию для оплаты и возвращает ID и ссылку."""
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/success/", # Заглушка
        cancel_url="http://localhost:8000/cancel/",   # Заглушка
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return {
        "session_id": session.id,
        "url": session.url
    }

def get_stripe_session_status(session_id: str) -> str:
    """Возвращает статус сессии (например, 'paid', 'unpaid')."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status
