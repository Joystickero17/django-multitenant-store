

class OrderStatusChoices:
    IN_CART = "IN_CART"
    VALIDATING_PAYMENT = "VALIDATING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CHOICES = [
        (IN_CART, "En el carrito"),
        (VALIDATING_PAYMENT, "validando pago"),
        (PAYMENT_FAILED, "pago_fallido")
    ]
