from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json
# Create your models here.

TICKER = []
with open("valids.json") as valids:
	valids = json.load(valids)

	for i in valids['valids']:
		TICKER.append((i['token'], i['token']))


class Coins(models.Model):
	ticker = models.CharField(max_length=8, null=True, choices=TICKER)
	name = models.CharField(max_length=20, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return str(self.ticker)

	class Meta:
		verbose_name_plural = "Coins"

class lostItem(models.Model):
	username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=1000, null=True)
	location = models.CharField(max_length=1000, null=True)
	description = models.CharField(max_length=1000, null=True)
	image = models.ImageField(upload_to = "images/")

class Acc_Positions(models.Model):
	username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	coin = models.CharField(max_length=8, default='', null=True, choices=TICKER) #do not drop max_length some symbols e.g. STARL are longer than 4 chars
	quantity = models.FloatField(default=None, null=True)
	price_per_coin = models.FloatField(null=True)
	time_bought = models.DateTimeField(null=True, default=datetime.now, blank=True)

	def __str__(self):
		return f"User: {self.username_id} Coin: {self.coin} " \
			   f"Quantity: {self.quantity} Price: {self.price_per_coin} " \
			   f"Time: {self.time_bought}"

	class Meta:
		verbose_name_plural = "ACC_Positions"


class coinPrices(models.Model):
	symbol = models.CharField(max_length=8, primary_key=True)
	name = models.CharField(max_length=20, null=True)
	derivedUSD = models.FloatField(default=None, null=True)
