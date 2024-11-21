from django.shortcuts import render, get_object_or_404
from .cart import Cart
from mystore.models import Products
from django.http import JsonResponse


def cart_summary(request):
    return render(request, "cart_summary.html", {})

def cart_add(request):
    # Obtain the cart data
    cart = Cart(request)
    # POST testing from action JS variable added in product.html
    if request.POST.get('action') == 'post':
        # Get the products
        product_id = int(request.POST.get('product_id'))
        # check if the product exists in DB
        product = get_object_or_404(Products, id=product_id)
        # Save the cart session
        cart.add(product=product)
        
        # return quantity to the page
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty: ': cart_quantity})
        
        return response

def cart_delete(request):
    pass
    
def cart_update(request):
    pass