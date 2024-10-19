from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Organization, Product, Transaction
from .forms import ProductForm, TransactionForm
from .ipfs_integration import add_to_ipfs, get_from_ipfs
from .solana_integration import send_transaction_sync
from .solana_integration import load_keypair_from_secret, send_transaction_sync


from django.core.exceptions import ValidationError
from django.contrib import messages



def product_list(request):
    products = Product.objects.all()
    return render(request, 'supply_chain/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product_data = {
                'name': product.name,
                'description': product.description,
                'quantity': product.quantity,
                'organization': product.current_organization.name,
            }
            ipfs_hash = add_to_ipfs(product_data)
            product.ipfs_hash = ipfs_hash
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'supply_chain/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    transactions = product.transactions.all().order_by('-timestamp')
    organization_hashes = [transaction.from_organization.org_hash for transaction in transactions] + [product.current_organization.org_hash]
    return render(request, 'supply_chain/product_detail.html', {
        'product': product,
        'transactions': transactions,
        'organization_hashes': organization_hashes
    })

def transfer_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.from_organization = product.current_organization
            try:
                transaction.save()
                product.current_organization = transaction.to_organization
                product.status = f"Transferred to {transaction.to_organization.name}"
                product.save()
                send_transaction_sync(transaction.transaction_hash)
                return redirect('product_detail', product_id=product.id)
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = TransactionForm()
    return render(request, 'supply_chain/transfer_product.html', {'form': form, 'product': product})

def get_ipfs_data(request, ipfs_hash):
    data = get_from_ipfs(ipfs_hash)
    return JsonResponse(data)
