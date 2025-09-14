import uuid
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id:  
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
