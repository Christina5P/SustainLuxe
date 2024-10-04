from django import forms
from .models import User


class SignupForm(forms.ModelForm):
    # Om du har extra fält kan du definiera dem här
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput
    )

    class Meta:
        model = User  # Byt ut mot den modell du vill använda
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]  # Exempel på fält

