from django.shortcuts import render, get_object_or_404
from .cart import Cart
from mystore.models import Products
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prod
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    return render(request, "cart_summary.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals})

def cart_add(request):
    # Obtain the cart data
    cart = Cart(request)
    # POST testing from action JS variable added in product.html
    if request.POST.get('action') == 'post':
        # Get the products
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # check if the product exists in DB
        product = get_object_or_404(Products, id=product_id)
        # Save the cart session
        cart.add(product=product, quantity=product_qty)
        
        # return cart quantity to the page
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        
        return response

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        # Get the products
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        
        response = JsonResponse({'product': product_id})
        return response
        
    
def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        # Get the products
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty': product_qty})
        return response
    
        