from django import forms

DISPLAY_CHOICES = (
    ("5", "5 Star"),
    ("4-4.9", "4 Star"),
    ("3-3.9", "3 Star"),
    ("2", "2 Star"),
    ("1", "1 Star"),
)

LOCATION_CHOICES =(
    ("local", "local"),
    ("Overseas", "Overseas"),
)
class MyForm(forms.Form):
    num_star = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=DISPLAY_CHOICES)
    location = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=LOCATION_CHOICES)
