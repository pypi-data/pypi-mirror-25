from culqipy.resource import (
    Token,
    Charge,
    Plan,
    Subscription,
    Refund,
    Iins,
    Card,
    Event,
    Customer,
    Transfer,
)
from culqipy.utils import Util

# Configuration variables.
API_URL_INTEG = "https://integ-pago.culqi.com/api/v1"
API_URL_PROD = "https://pago.culqi.com/api/v1"
llave_publica = None
llave_privada = None
