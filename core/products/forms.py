from django import forms 
from .models import Products

class ProductUploadForms(forms.ModelForm):

    class Meta:
        model = Products 
        fields = [
            'product_name', 'product_price', 'product_quantity', 'product_image'
        ] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product_image'].widget.attrs.update({'accept':'image/*'}) 

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
            