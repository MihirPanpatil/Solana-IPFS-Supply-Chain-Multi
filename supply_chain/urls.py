from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/transfer/', views.transfer_product, name='transfer_product'),
    path('ipfs/<str:ipfs_hash>/', views.get_ipfs_data, name='get_ipfs_data'),
]
