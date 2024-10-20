from django import forms
from .models import UserProfile
from products.models import Product, Size, Condition


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
                self.fields[field].widget.attrs[
                    'class'
                ] = 'border-black rounded-0 profile-form-input'


class SellerForm(forms.ModelForm):

    PAY_FOR_RETURN_SHIPPING = 'pay_for_return'
    DONATE_UNSOLD = 'donate_unsold'

    RETURN_OPTIONS = [
        (PAY_FOR_RETURN_SHIPPING, 'Pay for a return shipping label'),
        (DONATE_UNSOLD, 'Donate unsold items'),
    ]

    full_name = forms.CharField(
        max_length=255,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
    )

    email = forms.EmailField( 
        max_length=255,
        required=True,
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}),
    )

    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your phone number'}
        ),
    )

    street_address = forms.CharField(
        max_length=255,
        required=True,
        label="Street Address",
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your street address'}
        ),
    )

    postcode = forms.CharField(
        max_length=10,
        required=True,
        label="Postal Code",
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your postal code'}
        ),
    )

    town_or_city = forms.CharField(
        max_length=100,
        required=True,
        label="Town or City",
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your town or city'}
        ),
    )

    name = forms.CharField(
        max_length=255,
        required=True,
        label="Product Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter product name'}),
    )
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
        required=False,
    )
    """
    SIZE = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
      
    ]

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        required=True,
        label="Size",
        widget=forms.Select(attrs={'placeholder': 'Enter size'}),
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter price'}),
    )

    CONDITION_CHOICES = [
        ('New with tags', 'New with tags'),
        ('Like new', 'Like new'),
        ('Excellent Condition', 'Excellent Condition'),
        ('Good Condition', 'Good Condition'),
        ('Acceptable', 'Acceptable'),
    ]

    condition = forms.ModelChoiceField(
        queryset=Condition.objects.all(),
        required=True,
        label="Condition",
        widget=forms.Select,
    )

    return_option = forms.ChoiceField(
        choices=RETURN_OPTIONS,
        widget=forms.RadioSelect,
        label="Return for unsold product?",
    )

    class Meta:
        model = Product
        fields = [
            'user',
            'full_name',
            'email',
            'phone_number',
            'street_address',
            'postcode',
            'town_or_city',
            'name',
            'price',
            'size',
            'condition',
            'return_option',
        ]

        def __init__(self, *args, **kwargs):
            user_profile = kwargs.pop('user_profile', None)
            super().__init__(*args, **kwargs)
            if user_profile:
                self.fields['seller'].initial = user_profile.id

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
