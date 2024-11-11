from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, Brand, Condition, Size
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit


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

        # Initiera FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'POST'  # Sätt formens metod till POST
        self.helper.form_action = ''  # Om du vill definiera en form-action här kan du göra det

        # Använd Layout för att styra hur fälten ska visas
        self.helper.layout = Layout(
            Div('image', css_class='form-group'),
            Div('categories', css_class='form-group'),
            Submit('submit', 'Add Product', css_class='btn btn-primary rounded-0')
        )

        # Ställ in fälten med en viss CSS-klass
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

        # Sätt kategorival till vänliga namn
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['categories'].choices = friendly_names


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
