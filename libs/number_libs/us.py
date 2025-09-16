import http.client
import json
from typing import List
from decimal import Decimal, ROUND_HALF_UP
from django.http import JsonResponse
from config.env import DAISYSMS_API_KEY
from urllib.parse import urlencode


def getnumber(request, service: str):
    """
    Fetch numbers from DaisySMS API.
    Required: service
    Optional: amount, areas (comma separated), carriers
    """

    service = service.lower()

    # Extract params
    amount = request.GET.get("amount")
    carriers = request.GET.get("carriers")  # e.g. "tmo"
    areas_param = request.GET.get("areas")  # e.g. "201,520"
    areas = areas_param.split(",") if areas_param else []

    # Calculate max price
    max_price = None
    if amount is not None:
        try:
            amount = int(amount)
            max_price = (amount - 800) / 1600
        except Exception:
            return JsonResponse({"error": "Invalid amount"}, status=400)

    # Build query params exactly as Daisy expects
    params = {
        "api_key": DAISYSMS_API_KEY,
        "action": "getNumber",
        "service": service,
    }
    if max_price is not None:
        params["max_price"] = f"{max_price:.2f}"  # formatted float string
    if carriers:
        params["carriers"] = carriers
    if areas:
        params["areas"] = ",".join(areas)

    query = "/stubs/handler_api.php?" + urlencode(params)

    full_url = f"https://daisysms.com{query}"

    # 👇 Print to console (for debugging)
    print("Constructed DaisySMS URL:", full_url)

    conn = http.client.HTTPSConnection("daisysms.com")
    try:
        conn.request("GET", query)
        response = conn.getresponse()
        raw_data = response.read().decode("utf-8")

        # DaisySMS error responses
        error_responses = {
            "MAX_PRICE_EXCEEDED": "Max price exceeded",
            "NO_NUMBERS": "No numbers available",
            "TOO_MANY_ACTIVE_RENTALS": "Finish some rentals before renting more",
            "NO_MONEY": "Not enough balance",
        }

        if raw_data in error_responses:
            return JsonResponse({"error": error_responses[raw_data]}, status=400)

        # Try parse JSON response
        try:
            data = json.loads(raw_data)
            structured_data = []

            for service_type, items in data.items():
                for key, item in items.items():
                    try:
                        cost = (Decimal(item.get("cost", "0")) * 1600 + 800).quantize(
                            Decimal("0.01"), rounding=ROUND_HALF_UP
                        )
                        ltr_price = (Decimal(item.get("ltrPrice", "0")) * 800).quantize(
                            Decimal("0.01"), rounding=ROUND_HALF_UP
                        )
                    except Exception:
                        cost, ltr_price = None, None

                    structured_data.append({
                        "name": item.get("name"),
                        "count": item.get("count"),
                        "ttl": item.get("ttl"),
                        "cost": float(cost) if cost else None,
                        "ltrPrice": float(ltr_price) if ltr_price else None,
                        "repeatable": item.get("repeatable"),
                    })

            return JsonResponse(structured_data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"number_info": raw_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        conn.close()


def getnumber_list(request):
    base_url = '/stubs/handler_api.php?'
    api_param = 'api_key='
    action = '&action=getPricesVerification'
    conn = http.client.HTTPSConnection("daisysms.com")
    url = f"{base_url}{api_param}{DAISYSMS_API_KEY}{action}"

    try:
        conn.request("GET", url)
        response = conn.getresponse()

        if response.status != 200:
            raise Exception(f"HTTP Error: {response.status}")

        raw_data = response.read()
        data = json.loads(raw_data.decode("utf-8"))

        structured = []
        for service_code, countries in data.items():
            for country_code, details in countries.items():
                try:
                    cost_naira = (float(details.get("cost", 0)) * 1600) + 800
                    ltr_price_naira = (float(details.get("ltrPrice", 0)) * 1600) + 800
                except Exception:
                    cost_naira = details.get("cost")
                    ltr_price_naira = details.get("ltrPrice")

                structured.append({
                    "service_code": service_code,
                    "service_name": details.get("name"),
                    "ttl": details.get("ttl"),
                    "count": details.get("count"),
                    "cost": cost_naira,
                    "ltrPrice": ltr_price_naira,
                    "repeatable": details.get("repeatable"),
                })

    except Exception as e:
        print("Error fetching API data:", e)
        structured = {"error": str(e)}
    finally:
        conn.close()

    return JsonResponse(structured, safe=False)


def rent_number(request, number_id):
    base_url = '/stubs/handler_api.php?'
    api_param = 'api_key='
    action = f'&action=getStatus&id=${number_id}'
    conn = http.client.HTTPSConnection("daisysms.com")
    url = f"{base_url}{api_param}{DAISYSMS_API_KEY}{action}"

    try :
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(f"HTTP Error: {response.status}")
        raw_data = response.read()
        data = json.loads(raw_data.decode("utf-8"))
        return JsonResponse(data)
    except Exception as e:
        print("Error fetching API data:", e)
        structured = {"error": str(e)}
    finally:
        conn.close()
    return JsonResponse(structured, safe=False)