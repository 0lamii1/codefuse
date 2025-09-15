import os
from dotenv import load_dotenv


load_dotenv()

PAYSTACK_KEY = str(os.getenv('PAYSTACK_KEY'))

DAISYSMS_API_KEY = str(os.getenv('DAISYSMS_API_KEY'))

PRODUCTION_KEY = str(os.getenv('PRODUCTION_KEY'))
LOCAL_KEY = str(os.getenv('LOCAL_KEY'))


DB_NAME = str(os.getenv("DB_NAME", "inquisitive-tomato-grasshopper"))
DB_USER = str(os.getenv("DB_USER", "squid"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD", "qI8+kH6_rP4-kK9+cT5="))
DB_HOST = str(os.getenv("DB_HOST", "europe-north1-001.proxy.kinsta.app"))
DB_PORT = str(os.getenv("DB_PORT", "30708"))
