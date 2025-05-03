from django import forms
from .models import Watch, Bid

#Watch Form
class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ['title', 'brand', 'description', 'condition', 'image', 'tags']

#Bid Form
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 1}),
        }