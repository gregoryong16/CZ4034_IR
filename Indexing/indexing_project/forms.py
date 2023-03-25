from django import forms

DISPLAY_CHOICES = (
    ("4.5", ">=4.5"),
    ("4", ">=4"),
    ("3", "Below 4")
)

LOCATION_CHOICES =(
    ("local", "Local"),
    ("overseas", "Overseas"),
)
class MyForm(forms.Form):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=DISPLAY_CHOICES)
    location = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=LOCATION_CHOICES)
