from django.db import models
import re

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['priority']  # Automatically order by priority when querying

    def save(self, *args, **kwargs):
        # User would be entering name as Currency Beacon,
        # but in DB, we would saving name as currency_beacon
        self.name = re.sub(r'\s+', '_', self.name.strip().lower())
        super().save(*args, **kwargs)