from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/transfer/', views.transfer_product, name='transfer_product'),
    path('ipfs/<str:ipfs_hash>/', views.get_ipfs_data, name='get_ipfs_data'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/certificate/', views.view_certificate, name='view_certificate'),
    path('ipfs-file/<str:ipfs_hash>/', views.serve_ipfs_file, name='serve_ipfs_file'),
]
