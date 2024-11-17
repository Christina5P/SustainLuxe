from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Brand, Condition, Size
# from crispy_forms.layout import Layout, Div, Submit


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()


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

        main_categories = Category.objects.filter(parent_categories=None)
        choices = []
        for main_cat in main_categories:
            choices.append((main_cat.id, main_cat.name))
            for sub_cat in main_cat.subcategories.all():
                choices.append((sub_cat.id, f"- {sub_cat.name}"))

        self.fields['categories'].choices = choices
