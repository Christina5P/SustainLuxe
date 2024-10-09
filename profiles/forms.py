from django import forms
from .models import User, UserProfile, Account


def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('some_view_name')
    else:
        form = CreateAccountForm()

    return render(request, 'profiles/create_account.html', {'form': form})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                placeholder = placeholders.get(field, field)
                if self.fields[field].required:
                    placeholder += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder

            
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'


class AccountForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True
    ) 
    sku = forms.CharField(
        max_length=100, required=False
    ) 

    class Meta:
        model = Account
        fields = [
            'user',
            'withdrawal_history',
        ]  
