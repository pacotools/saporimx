from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()

        # This special syntax is called list comprehension
        # It's a shorthand way of creating a for loop that adds items to a list
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Now that we have the friendly names, let's update the category field
        # on the form to use those choices instead of using the id.
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
