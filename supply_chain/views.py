from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Organization, Product, Transaction
from .forms import ProductForm, TransactionForm
from .ipfs_integration import add_to_ipfs, get_from_ipfs
from .solana_integration import send_transaction_sync
from .solana_integration import load_keypair_from_secret, send_transaction_sync

from solana.exceptions import SolanaRpcException
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse
from django.http import FileResponse

from django.http import HttpResponse
from PIL import Image
import io
from django.utils import timezone
import pytz
from .ipfs_integration import get_from_ipfs

def get_ist_time():
    return timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))

def product_list(request):
    products = Product.objects.all()
    return render(request, 'supply_chain/product_list.html', {'products': products})

def welcome(request):
    return render(request, 'supply_chain/welcome.html')

from django.core.files.base import ContentFile

from .ipfs_integration import add_file_to_ipfs, add_to_ipfs

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.timestamp = get_ist_time()
            product_data = {
                'name': product.name,
                'description': product.description,
                'quantity': product.quantity,
                'organization': product.current_organization.name,
            }
            
            # Handle certificate upload
            if 'certificate' in request.FILES:
                certificate_file = request.FILES['certificate']
                certificate_ipfs_hash = add_file_to_ipfs(certificate_file)
                if certificate_ipfs_hash:
                    product.certificate_ipfs_hash = certificate_ipfs_hash
                else:
                    form.add_error('certificate', "Failed to upload certificate to IPFS.")
                    return render(request, 'supply_chain/add_product.html', {'form': form})

            # Add product data to IPFS
            product_ipfs_hash = add_to_ipfs(product_data)
            if product_ipfs_hash:
                product.ipfs_hash = product_ipfs_hash
                product.save()
                return redirect('product_list')
            else:
                form.add_error(None, "Failed to add product data to IPFS. Please try again.")
    else:
        form = ProductForm()
    return render(request, 'supply_chain/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    transactions = Transaction.objects.filter(product=product).order_by('timestamp')
    
    organization_hashes = []
    for transaction in transactions:
        organization_hashes.append({
            'from': transaction.from_organization.org_hash,
            'to': transaction.to_organization.org_hash,
            'timestamp': transaction.timestamp
        })
    
    # Add the current organization as the final 'to' hash
    if organization_hashes:
        organization_hashes.append({
            'from': organization_hashes[-1]['to'],
            'to': product.current_organization.org_hash,
            'timestamp': product.timestamp
        })
    else:
        # If no transactions, just show the current organization
        organization_hashes.append({
            'from': None,
            'to': product.current_organization.org_hash,
            'timestamp': product.timestamp
        })

    context = {
        'product': product,
        'transactions': transactions,
        'organization_hashes': organization_hashes,
    }
    return render(request, 'supply_chain/product_detail.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import TransactionForm

def transfer_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, product=product)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.timestamp = get_ist_time()
            transaction.product = product
            transaction.from_organization = product.current_organization
            transaction.save()
            
            product.current_organization = transaction.to_organization
            product.status = 'Transferred'
            product.save()
            
            return redirect('product_detail', product_id=product.id)
    else:
        form = TransactionForm(product=product)
    
    return render(request, 'supply_chain/transfer_product.html', {'form': form, 'product': product})

from django.http import JsonResponse
import json

from django.http import JsonResponse, FileResponse
from django.core.files.base import ContentFile
import json
import magic

def get_ipfs_data(request, ipfs_hash):
    data = get_from_ipfs(ipfs_hash)
    
    # Use python-magic to detect the MIME type
    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(data)

    if content_type.startswith('application/json'):
        # It's JSON data
        try:
            json_data = json.loads(data)
            return JsonResponse(json_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        # It's binary data (like an image or PDF)
        return FileResponse(ContentFile(data), content_type=content_type)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' has been deleted.")
        return redirect('product_list')
    return render(request, 'supply_chain/confirm_delete.html', {'product': product})

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

def view_certificate(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.certificate:
        if product.certificate.name.lower().endswith('.pdf'):
            # For PDF files, we'll just return the file
            return FileResponse(product.certificate.open(), content_type='application/pdf')
        else:
            # For image files, we'll use Pillow to open and display
            img = Image.open(product.certificate.path)
            response = HttpResponse(content_type="image/jpeg")
            img.save(response, "JPEG")
            return response
    else:
        messages.error(request, "No certificate found for this product.")
        return redirect('product_detail', product_id=product.id)
    
from django.http import FileResponse

def serve_ipfs_file(request, ipfs_hash):
    file_content = get_from_ipfs(ipfs_hash)
    return FileResponse(ContentFile(file_content), content_type='application/pdf')
