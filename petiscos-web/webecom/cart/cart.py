from mystore.models import Products, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # get the request
        self.request = request
        # get the session key
        cart = self.session.get('session_key')
        # or create one if there isn't one:
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}    
        
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        # User logged in (In order to save the user cart.)
        if self.request.user.is_authenticated:
            # Get the current user profile.
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert the cart dictionary to json format string e.g {product_id: '3':2 to "3":2}.
            convert_cart = str(self.cart)
            convert_cart = convert_cart.replace("\'","\"")
            current_user.update(old_cart=str(convert_cart))
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        # User logged in (In order to save the user cart.)
        if self.request.user.is_authenticated:
            # Get the current user profile.
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert the cart dictionary to json format string e.g {product_id: '3':2 to "3":2}.
            convert_cart = str(self.cart)
            convert_cart = convert_cart.replace("\'","\"")
            current_user.update(old_cart=str(convert_cart))
            
            
            
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
          
        for key, value in quantities.items():
            key = int(key)
            
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        
        return total    
    
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
         
        # User logged in (In order to save the user cart.)
        if self.request.user.is_authenticated:
            # Get the current user profile.
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert the cart dictionary to json format string e.g {product_id: '3':2 to "3":2}.
            convert_cart = str(self.cart)
            convert_cart = convert_cart.replace("\'","\"")
            current_user.update(old_cart=str(convert_cart))
        
        usercartupd = self.cart
        
        return usercartupd
    
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        # User logged in (In order to save the user cart.)
        if self.request.user.is_authenticated:
            # Get the current user profile.
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert the cart dictionary to json format string e.g {product_id: '3':2 to "3":2}.
            convert_cart = str(self.cart)
            convert_cart = convert_cart.replace("\'","\"")
            current_user.update(old_cart=str(convert_cart))