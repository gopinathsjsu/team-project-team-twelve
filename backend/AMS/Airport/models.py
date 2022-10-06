from django.db import models

# Create your models here.
import uuid
class Mio_user(models.Model):
    fact_guid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id=models.CharField(max_length=200)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=64)
    is_active=models.BooleanField(default=False)
