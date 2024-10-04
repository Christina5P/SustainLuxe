from django import forms


class SignupForm(forms.Form):
    signonname = forms.CharField(max_length=100, required=True)
    signonusername = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    signonpassword = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    newsletter = forms.BooleanField(required=False)
