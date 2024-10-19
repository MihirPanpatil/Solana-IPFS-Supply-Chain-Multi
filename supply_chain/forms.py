from django import forms
from .models import Product, Transaction, Organization, ORGANIZATION_TYPES

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'current_organization', 'certificate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_organization'].queryset = Organization.objects.filter(org_type='FARM')

from django import forms
from .models import Transaction, Organization, Product

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['to_organization']

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if self.product:
            current_org_type = self.product.current_organization.org_type
            if current_org_type == 'DISTRIBUTION':
                # Allow transfer to retailers when at distribution stage
                self.fields['to_organization'].queryset = Organization.objects.filter(org_type='RETAIL')
            else:
                next_org_type = self.get_next_org_type(current_org_type)
                self.fields['to_organization'].queryset = Organization.objects.filter(org_type=next_org_type)

    def get_next_org_type(self, current_org_type):
        org_types = dict(Organization.ORG_TYPES)
        org_type_list = list(org_types.keys())
        current_index = org_type_list.index(current_org_type)
        if current_index < len(org_type_list) - 1:
            return org_type_list[current_index + 1]
        elif current_org_type == 'DISTRIBUTION':  # If it's the distribution org
            return 'RETAIL'  # Allow transfer to retail
        return None

    def clean(self):
        cleaned_data = super().clean()
        to_organization = cleaned_data.get('to_organization')

        if self.product and to_organization:
            if not self.product.can_transfer_to(to_organization):
                raise forms.ValidationError("Invalid transfer. Check organization types.")

        return cleaned_data