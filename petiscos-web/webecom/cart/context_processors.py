from .cart import Cart

# making sure the cart works for every page.

def cart(request):
    return {'cart': Cart(request)}