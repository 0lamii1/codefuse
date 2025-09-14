import random
from django.db import models
from utilities.base_model import BaseModel
from user.models import User
from decimal import Decimal

def unique_id(k=10):
    return ''.join(str(random.randint(0, 9)) for _ in range(k))

class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wallet")
    wallet_id = models.CharField(max_length=20, null=True, unique=True, default=unique_id)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return self.user.username

