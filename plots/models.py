from django.db import models
from datetime import datetime
# Create your models here.

class HistoricalPrices(models.Model):
    intTime = models.BigIntegerField()
    token = models.CharField(max_length=10)
    price = models.FloatField()

    def __str__(self):
        return "Time: " + str(datetime.fromtimestamp(float(self.intTime))) + \
               " Token: " + str(self.token) + \
               " Price: " + str(self.price)