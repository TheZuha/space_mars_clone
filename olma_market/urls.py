from .views import detail_page, category_products, purchase_view, add_to_cart, view_cart, product_list, stores_list
from django.urls import path

urlpatterns = [
    path('', product_list, name='home'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('product/<int:id>/', detail_page, name='detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('purchase/<int:product_id>/', purchase_view, name='purchase'),
    path('products/', product_list, name='product_list'),
    path('stores/', stores_list, name='stores_list'),
]
