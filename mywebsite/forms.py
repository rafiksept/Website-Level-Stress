from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from story.models import Gambar , Komentar
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save
        return user
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Gambar
        fields = ["foto",]

class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ["coment","anonymous"]