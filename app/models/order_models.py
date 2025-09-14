from django.db import models
import enum
from utilities.base_model import BaseModel
from user.models import User
from .transaction_models import Transaction

class OrderStatus(str, enum.Enum):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    service = models.CharField(max_length=155)
    country = models.CharField(max_length=55, null=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    code = models.CharField(max_length=6, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=[(status.value, status.value) for status in OrderStatus],default=OrderStatus.PENDING.value) 
    has_recieved_code = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.user.username



