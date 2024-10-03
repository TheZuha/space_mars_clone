from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Categories, Cart, CartItem, Store
from users.models import Orders
from .forms import OrderForm
from django.utils import timezone



def purchase_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Umumiy narxni hisoblash
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            delivery_method = form.cleaned_data['delivery_method']
            payment_method = form.cleaned_data['payment_method']

            # Mahsulot countni tekshirish
            if product.count > 0:
                product.count -= 1
                product.save()

                # Buyurtma yaratish
                order = Orders.objects.create(
                    order_id=product_id,
                    total_price=total_price,  # umumiy narx
                    date_of_delivery=timezone.now() if delivery_method == 'pickup' else None,
                    shop_id=form.cleaned_data['shops'] if delivery_method == 'pickup' else None,
                    payment_type=payment_method,
                    user_id=request.user.id,
                    order_date=timezone.now()
                )

                if payment_method == 'card':
                    card_number = form.cleaned_data['card_number']
                    card_expiry_date = form.cleaned_data['card_expiry_date']
                    print(f"Karta raqami: {card_number}, Amaliy sanasi: {card_expiry_date}")

                CartItem.objects.filter(cart=cart).delete()
                return redirect('home')
            else:
                form.add_error(None, "Mahsulot mavjud emas")
    else:
        form = OrderForm()

    return render(request, 'purchase.html', {
        'form': form,
        'product': product,
        'cart_items': cart_items,
        'total_price': total_price
    })


def detail_page(request, id):
    product = get_object_or_404(Products, id=id)
    context = {'product': product}
    return render(request, 'detail.html', context=context)


# def category_list(request):
#     categories = Categories.objects.all()  # Barcha kategoriyalarni olish
#     products = Products.objects.all()  # Barcha mahsulotlarni olish
#     context = {
#         'categories': categories,
#         'products': products
#     }
#     return render(request, 'category_list.html', context)  # Buni sizning HTML faylingizga moslang


def category_products(request, category_id):
    categories = Categories.objects.all()  # Barcha kategoriyalarni olish
    category = get_object_or_404(Categories, id=category_id)  # Ma'lum bir kategoriyani olish
    products = Products.objects.filter(category=category)  # Ushbu kategoriyaga tegishli mahsulotlarni olish
    context = {
        'categories': categories,
        'products': products,
        'selected_category': category
    }
    return render(request, 'category_products.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('view_cart')


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    context = {
        'cart_items': cart_items,
        'total_price': cart.total_price()
    }
    return render(request, 'cart.html', context)



def product_list(request):
    products = Products.objects.all()
    categories = Categories.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'selected_category': None,
    }
    return render(request, 'category_list.html', context)


def stores_list(request):
    shops = Store.objects.all()
    context = {
            'shops': shops,
    }
    return render(request, 'stores.html', context)