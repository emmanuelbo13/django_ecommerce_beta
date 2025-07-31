import mercadopago
from django.conf import settings

class MercadoPagoService:
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    def create_preference(self, cart, shipping_address):
        items = []
        for item in cart:
            items.append(
                {
                    "title": item['product'].name,
                    "quantity": item['quantity'],
                    "unit_price": float(item['product'].price),
                }
            )

        preference_data = {
            "items": items,
            "payer": {
                "name": shipping_address.user.first_name,
                "surname": shipping_address.user.last_name,
                "email": shipping_address.user.email,
                "address": {
                    "street_name": shipping_address.address_line_1,
                    "street_number": shipping_address.address_line_2,
                    "zip_code": shipping_address.postal_code,
                },
            },
            "back_urls": {
                "success": settings.MERCADO_PAGO_SUCCESS_URL,
                "failure": settings.MERCADO_PAGO_FAILURE_URL,
                "pending": settings.MERCADO_PAGO_PENDING_URL,
            },
            "auto_return": "approved",
        }

        preference_response = self.sdk.preference().create(preference_data)
        return preference_response

    def get_payment_status(self, payment_id):
        payment_info = self.sdk.payment().get(payment_id)
        return payment_info["response"]["status"]