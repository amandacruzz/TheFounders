from django.forms import ModelForm
from django import forms
from .models import Acc_Positions, lostItem

class Lost_Item_Form(forms.ModelForm):
	class Meta:
		model = lostItem
		fields = ['title', 'location', 'description', 'image']