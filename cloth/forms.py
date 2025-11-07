from django import forms
from .models import Cloth

class ClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = ['name', 'description', 'price', 'image']
