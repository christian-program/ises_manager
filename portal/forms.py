from django import forms
from django.contrib.auth.models import User

class SimpleRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'placeholder': 'Ex: Christian'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe'}))
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Répétez le mot de passe'}))

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas.")
        return cleaned_data