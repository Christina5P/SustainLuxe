from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Brand, Condition, Size


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
    )
    Category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['categories'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ProductFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    conditions = forms.ModelMultipleChoiceField(
        queryset=Condition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        main_categories = Category.objects.filter(parent_category=None)
        choices = []
        for main_cat in main_categories:
            choices.append((main_cat.id, main_cat.name))
            for sub_cat in main_cat.subcategories.all():
                choices.append((sub_cat.id, f"- {sub_cat.name}"))
    
        self.fields['categories'].choices = choices