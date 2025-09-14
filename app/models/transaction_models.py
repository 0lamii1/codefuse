import uuid
from django.db import models
from user.models import User
from utilities.base_model import BaseModel
from .wallet_models import Wallet



class Transaction(BaseModel):
    class TransactionType(models.TextChoices):
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    class TransactionStatus(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        PENDING = "PENDING", "Pending"
        CANCELLED = "CANCELLED", "Cancelled"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=22, unique=True, null=True)
    

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.status}"
