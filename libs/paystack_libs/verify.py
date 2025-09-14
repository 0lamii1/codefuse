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
from libs.paystack_libs.base_service import update_wallet_transaction

logger = logging.getLogger(__name__)


def verify_paystack_transaction(reference: str):
    try:
        conn = http.client.HTTPSConnection("api.paystack.co")
        headers = {
            "Authorization": f"Bearer {PAYSTACK_KEY}",
            "Content-Type": "application/json"
        }
        conn.request("GET", f"/transaction/verify/{reference}", headers=headers)

        response = conn.getresponse()
        data = orjson.loads(response.read())
        conn.close()

        if data.get('status') and data['data']['status'] == "success":
            Transaction(status='success', reference=reference)
            return {
                'success': True,
                'message': 'Payment verified successfully.',
                'reference': reference
            }

        update_wallet_transaction(status=data['data']['status'], reference=reference)
        return {
            'success': False,
            'message': f"Payment verification failed. Status: {data['data']['status']}",
            'reference': reference
        }

    except Exception as e:
        return {
            'success': False,
            'message': 'Error occurred while verifying transaction.',
            'reference': reference,
            'error': str(e)
        }

