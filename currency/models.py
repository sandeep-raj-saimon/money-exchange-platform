from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return f"{self.name}"
