from mystore.models import Products

class Cart():
    def __init__(self, request):
        self.session = request.session
        # get the session key
        cart = self.session.get('session_key')
        # or create one if there isn't one:
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}    
        
        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
    
    # Count for the cart
    def __len__(self):
        return len(self.cart)
    
    def get_prod(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids) 
        return products   
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        usercart = self.cart
        usercart[product_id] = product_qty
        
        self.session.modified = True
        
        usercartupd = self.cart
        return usercartupd