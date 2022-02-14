from .models import Cerita
from django import forms

class FormCerita(forms.ModelForm):
    judul = forms.CharField(
        widget = forms.Textarea(attrs={'placeholder':'ketik judul', 'maxlength':'300'})

    )
    class Meta:
        model = Cerita
        fields = [
            'judul',
            'isi',
            'is_publish',
            'anonymous'
        ]

        widgets = {
            'isi': forms.Textarea(attrs={
                'placeholder':'tulis ceritamu disini!'
            })
        }
        

