from django import forms
from .models import MediaItem

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'description', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Enter title'
            }),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10})
            
        }