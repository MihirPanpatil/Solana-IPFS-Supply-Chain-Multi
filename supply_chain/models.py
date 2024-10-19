from django.db import models
import hashlib
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ORGANIZATION_TYPES = [
    ('FARM', 'Farm'),
    ('PROCESSING', 'Processing Unit'),
    ('DISTRIBUTION', 'Distribution Unit'),
    ('RETAILER', 'Retailer'),
]

ORGANIZATION_TYPE_ORDER = ['FARM', 'PROCESSING', 'DISTRIBUTION', 'RETAILER']

class Organization(models.Model):
    ORG_TYPES = [
        ('FARM', 'Farm'),
        ('PROCESSING', 'Processing Unit'),
        ('DISTRIBUTION', 'Distribution Unit'),
        ('RETAIL', 'Retailer')
    ]

    name = models.CharField(max_length=100)
    org_type = models.CharField(max_length=20, choices=ORG_TYPES)
    org_hash = models.CharField(max_length=64, unique=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"

    def save(self, *args, **kwargs):
        if not self.org_hash:
            self.org_hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def calculate_hash(self):
        data = f"{self.name}{self.org_type}"
        return hashlib.sha256(data.encode()).hexdigest()
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Created')
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    certificate_ipfs_hash = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    quantity = models.FloatField(help_text="Quantity in Kg", default=0)
    current_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='current_products')
    ipfs_hash = models.CharField(max_length=100, blank=True)
    product_hash = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

    def calculate_hash(self):
        data = f"{self.name}{self.description}{self.current_organization.id}{self.ipfs_hash}{self.quantity}{self.status}"
        return hashlib.sha256(data.encode()).hexdigest()

    def save(self, *args, **kwargs):
        self.product_hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def can_transfer_to(self, to_organization):
        current_org_type = self.current_organization.org_type
        to_org_type = to_organization.org_type
    
        # Define the valid transfer chain
        transfer_chain = ['FARM', 'PROCESSING', 'DISTRIBUTION', 'RETAIL']
    
        current_index = transfer_chain.index(current_org_type)
        to_index = transfer_chain.index(to_org_type)
    
        # Check if the transfer is to the next organization type in the chain
        return to_index == current_index + 1

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    from_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='incoming_transactions')
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=64, blank=True)
    from_org_hash = models.CharField(max_length=64, blank=True)
    to_org_hash = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.product.name}: {self.from_organization.name} -> {self.to_organization.name}"

    def calculate_hash(self):
        data = f"{self.product.id}{self.from_organization.id}{self.to_organization.id}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()

    def save(self, *args, **kwargs):
        if not self.product.can_transfer_to(self.to_organization):
            raise ValidationError("Invalid transfer. Products can only be transferred to the next organization type in the chain.")
        self.transaction_hash = self.calculate_hash()
        self.from_org_hash = self.from_organization.org_hash
        self.to_org_hash = self.to_organization.org_hash
        super().save(*args, **kwargs)
