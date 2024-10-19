from django import forms
from .models import Product, Transaction, Organization, ORGANIZATION_TYPES

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'certificate', 'current_organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_organization'].queryset = Organization.objects.filter(org_type='FARM')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['to_organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_organization'].queryset = Organization.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        to_organization = cleaned_data.get('to_organization')
        if to_organization:
            product = self.instance.product
            if not product.can_transfer_to(to_organization):
                raise forms.ValidationError("Invalid transfer. Products can only be transferred to the next organization type in the chain.")
        return cleaned_data
