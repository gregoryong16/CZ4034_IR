from django import forms

DISPLAY_CHOICES = (
    ("5", "5"),
    ("4", "4 to 4.9"),
    ("3", "3 to 3.9"),
    ("2", "Below 3"),
)

LOCATION_CHOICES =(
    ("local", "Local"),
    ("Overseas", "Overseas"),
)
class MyForm(forms.Form):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=DISPLAY_CHOICES)
    location = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=LOCATION_CHOICES)
