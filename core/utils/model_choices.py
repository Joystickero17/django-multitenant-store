

class DeliveryTypeChoices:
    DELIVERY = "delivery"
    PERSONALLY = "personally"
    CHOICES = [
        (DELIVERY, "Delivery o Envio"),
        (PERSONALLY, "Retiro Personalmente")
    ]

class OrderStatusChoices:
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    VALIDATING_PAYMENT = "VALIDATING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAYMENT_EXPIRED = "PAYMENT_EXPIRED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    CHOICES = [
        (AWAITING_PAYMENT, "Esperando por pago del cliente"),
        (VALIDATING_PAYMENT, "validando pago"),
        (PAYMENT_FAILED, "Pago Fallido"),
        (PAYMENT_EXPIRED, "Pago Expirado"),
        (PAYMENT_SUCCESS, "Pago Exitoso"),
    ]

class PaymentMethodChoices:
    PAYPAL = "paypal"
    COINBASE = "coinbase"
    PAGO_MOVIL = "pago_movil"
    FREE_ITEM = "free_item"
    CHOICES = [
        (PAYPAL,"Paypal"),
        (COINBASE, "Coinbase crypto"),
        (PAGO_MOVIL, "Pago Movil"),
        (FREE_ITEM, "Productos Gratuitos"),
    ]

class NationalBankChoices:
    BANCO_DE_VENEZUELA="0102"
    BANCO_VENEZOLANO_DE_CREDITO="0104"
    BANCO_MERCANTIL="0105"
    BANCO_PROVINCIAL="0108"
    BANCARIBE="0114"
    BANCO_EXTERIOR="0115"
    BANCO_CARONI="0128"
    BANESCO_BANCO_UNIVERSAL="0134"
    SOFITASA="0137"
    BANCO_PLAZA="0138"
    BANGENTE="0146"
    BANCO_FONDO_COMUN="0151"
    CIEN_POR_CIENTO_BANCO="0156"
    DEL_SUR_BANCO_UNIVERSAL="0157"
    BANCO_DEL_TESORO="0163"
    BANCO_AGRICOLA_DE_VENEZUELA="0166"
    BANCRECER="0168"
    BANCO_MICROFINANCIERO="0169"
    BANCO_ACTIVO="0171"
    BANCAMIGA="0172"
    BANPLUS="0174"
    BANCO_BICENTENARIO_DEL_PUEBLO="0175"
    BANFANB="0177"
    BANCO_NACIONAL_DE_CREDITO="0191"
    CHOICES = [
        (BANCO_DE_VENEZUELA,"Banco de Venezuela (BDV)"),
        (BANCO_VENEZOLANO_DE_CREDITO,"Banco Venezolano de Crédito (BVC)"),
        (BANCO_MERCANTIL,"Banco Mercantil"),
        (BANCO_PROVINCIAL,"Banco Provincial (BBVA)"),
        (BANCARIBE,"Bancaribe"),
        (BANCO_EXTERIOR,"Banco Exterior"),
        (BANCO_CARONI,"Banco Caroní"),
        (BANESCO_BANCO_UNIVERSAL,"Banesco Banco Universal"),
        (SOFITASA,"Sofitasa"),
        (BANCO_PLAZA,"Banco Plaza"),
        (BANGENTE,"Bangente"),
        (BANCO_FONDO_COMUN,"Banco Fondo Común (BFC)"),
        (CIEN_POR_CIENTO_BANCO,"100% Banco"),
        (DEL_SUR_BANCO_UNIVERSAL,"Del Sur Banco Universal"),
        (BANCO_DEL_TESORO,"Banco del Tesoro"),
        (BANCO_AGRICOLA_DE_VENEZUELA,"Banco Agrícola de Venezuela"),
        (BANCRECER,"Bancrecer"),
        (BANCO_MICROFINANCIERO,"Mi Banco, Banco Microfinanciero C.A"),
        (BANCO_ACTIVO,"Banco Activo"),
        (BANCAMIGA,"Bancamiga"),
        (BANPLUS,"Banplus"),
        (BANCO_BICENTENARIO_DEL_PUEBLO,"Banco Bicentenario del Pueblo"),
        (BANFANB,"Banco de la Fuerza Armada Nacional Bolivariana (BANFANB)"),
        (BANCO_NACIONAL_DE_CREDITO,"Banco Nacional de Crédito (BNC)"),
    ]

class PricingTypeChoices:
    NO_PRICE = "no_price"
    FIXED_PRICE = "fixed_price"


class CurrencyChoices:
    # local
    VES = "VES"
    USD = "USD"
    # crypto
    BITCOIN = "BTC"
    ETHEREUM = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    DOGE = "DOGE"
    BITCOIN_CASH = "BCH"
    DAI = "DAI"
    LTC = "LTC"
    POLYGON = "PMATIC"
    PUSDC = "PUSDC"
    PWETH = "PWETH"
    SHIBAINU = "SHIB"