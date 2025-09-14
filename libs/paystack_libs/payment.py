import http.client
import orjson
import hmac
import logging
import hashlib
from config.env import PAYSTACK_KEY
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Transaction

logger = logging.getLogger(__name__)

def checkout(email: str, amount: Decimal):
    url = "api.paystack.co"
    endpoint = "/transaction/initialize"

    body = orjson.dumps({
        "email": email,
        "amount": int(amount * 100)  
    })

    headers = {
        "Authorization": f"Bearer {PAYSTACK_KEY}",
        "Content-Type": "application/json"
    }

    conn = http.client.HTTPSConnection(url)
    conn.request("POST", endpoint, body, headers)

    response = conn.getresponse()
    response_data = response.read()

    conn.close()

    try:
        parsed_data = orjson.loads(response_data)

        if parsed_data.get("status") and "data" in parsed_data:
            return {
                "reference": parsed_data["data"]["reference"],
                "authorization_url": parsed_data["data"]["authorization_url"]
            }
        else:
            return {
                "error": True,
                "message": parsed_data.get("message", "Failed to initialize transaction")
            }

    except Exception as e:
        return {
            "error": True,
            "message": "Invalid response from Paystack",
            "details": str(e)
        }







