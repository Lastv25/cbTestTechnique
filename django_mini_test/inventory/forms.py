from django import forms
from .models import Inventory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        # Ce champ gere la creation de inputFields dans la page add
        fields = [ 
            #'name',  
            'gtin',
            'expiry_date'
        ]
