import os
from dotenv import load_dotenv


load_dotenv()

PAYSTACK_KEY = str(os.getenv('PAYSTACK_KEY'))

DAISYSMS_API_KEY = str(os.getenv('DAISYSMS_API_KEY'))

PRODUCTION_KEY = str(os.getenv('PRODUCTION_KEY'))
LOCAL_KEY = str(os.getenv('LOCAL_KEY'))