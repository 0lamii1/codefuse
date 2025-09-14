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


@csrf_exempt
def paystack_webhook(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)
    body = request.body
    secret = PAYSTACK_KEY.encode('utf-8')
    computed_hmac = hmac.new(secret, body, hashlib.sha512).hexdigest()
    incoming_signature = request.headers.get('x-paystack-signature', '')
    if not hmac.compare_digest(computed_hmac, incoming_signature):
        return HttpResponse("Invalid signature", status=401)
    
    try:
        event = orjson.loads(body)
        event_data = event.get('data', {})
        reference = event_data.get('reference')
        status = event_data.get('status')
        
        transaction = Transaction.objects.filter(reference=reference).first()
        if transaction:
            if status == "success":
                update_wallet_transaction(status=status, reference=reference)
            elif status == "failed":
                update_wallet_transaction(status=status, reference=reference)
            else:
                update_wallet_transaction(status=status, reference=reference)
        return JsonResponse({"status": "success"})
    
    except Exception as error:
        return JsonResponse({"error": f"Unknown erro: {error}"}, status=400)
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Webhook processing error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    
