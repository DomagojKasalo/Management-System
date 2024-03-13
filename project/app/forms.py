from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik, Uloge, Predmeti, Upis
from django.contrib.auth.hashers import make_password

class CreateUserForm(UserCreationForm):
    uloge = forms.ModelChoiceField(queryset=Uloge.objects.all())

    class Meta(UserCreationForm.Meta):
        model = Korisnik
        fields = ['username', 'password1', 'password2', 'status', 'uloge']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uloge'].label = 'Uloga'

class PredmetiForm(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kod': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'ects': forms.TextInput(attrs={'class': 'form-control'}),
            'sem_red': forms.TextInput(attrs={'class': 'form-control'}),
            'sem_izv': forms.TextInput(attrs={'class': 'form-control'}),
            'izborni': forms.Select(attrs={'class': 'form-control'}),
            'nositelj': forms.Select(attrs={'class': 'form-control'})
        }

class AssignForm(forms.Form):
    profesor = forms.ModelChoiceField(queryset=Korisnik.objects.filter(uloge__uloga='profesor'))
    predmet = forms.ModelChoiceField(queryset=Predmeti.objects.all())

class KorisnikForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['first_name', 'last_name', 'username', 'status', 'uloge']

class UpisniForm(forms.ModelForm):
    class Meta:
        model = Upis
        fields = '__all__'  

class StatusForm(forms.ModelForm):
    class Meta:
        model = Upis
        fields = ['status']  
  
