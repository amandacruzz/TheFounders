from django.forms import ModelForm
from django import forms
from .models import Acc_Positions, lostItem

class Acc_Positions_Form(forms.ModelForm):
	class Meta:
		model = Acc_Positions
		fields = ['coin', 'quantity', 'price_per_coin', 'time_bought']
		'''
		widgets = {
			'coin': forms.Select(attrs={'class': 'form-control', 'placeholder':"Coins"}),
			'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Quantity' }),
			'price_per_coin': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Price Per Coin"}),
			'time_bought': forms.DateTimeField(attrs={'class': 'form-control', 'placeholder':""}, required=False)
		}
		'''

class Lost_Item_Form(forms.ModelForm):
	class Meta:
		model = lostItem
		fields = ['title', 'location', 'description', 'image']