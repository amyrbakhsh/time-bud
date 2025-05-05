from django import forms
from .models import Watch, Bid, Tag

#Watch Form
class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ['title', 'brand', 'description', 'condition', 'image', 'tags', 'is_available']
        widgets = {
            'tags': forms.CheckboxSelectMultiple
            
        }

#Bid Form
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 1}),
        }