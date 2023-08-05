from django.db import models

# Create your models here.

class Counter(models.Model):
    name_row = models.CharField(primary_key=True,max_length=15)
    total_max_hits = models.PositiveIntegerField(default=0)