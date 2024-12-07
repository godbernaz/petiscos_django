from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from mystore.models import Profile
	
def orders(request, pk):
    
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order.
        order = Order.objects.get(id=pk)
        # Get the order items.
        items = OrderItem.objects.filter(order=pk)
        
        if request.method == "POST":
            # Get the order status.
            status = request.POST['shipping_status']
            
			# Logic to change the order status.
            if status == "True":  
                order.shipped = True
            else:
                order.shipped = False
            
            order.save()  # Salva o objeto após a modificação
            messages.success(request, "O estado do pedido foi alterado!")
            return redirect('home')

        return render(request, 'payment/orders.html', {"order": order, "items": items})
        
    else:    
        messages.success(request, "Acesso Negado!")
        return redirect('home')
 
def not_shipped_dash(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        
        if request.method == "POST":
            
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=True)
            messages.success(request, "O estado do pedido foi alterado!")
            return redirect('not_shipped_dash')
        
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')

def shipped_dash(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        
        if request.method == "POST":
            
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
            
            messages.success(request, "O estado do pedido foi alterado!")
            return redirect('shipped_dash')  
        
        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')
 
def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prod
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # Registered Users.
            user = request.user
            # Create Order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                address=shipping_address,  # Use 'address' instead of 'shipping_address'
                amount_paid=amount_paid
            )
            create_order.save()

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            for product in cart_products():
                product_id = product.id
                # Get the sale/non_sale price for each product.
                price = product.sale_price if product.is_sale else product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")

            messages.success(request, "Pedido Confirmado!")
            return redirect('home')

        else:
            # Unregistered Users.
            create_order = Order(
                full_name=full_name,
                email=email,
                phone=phone,
                address=shipping_address,  # Use 'address' instead of 'shipping_address'
                amount_paid=amount_paid
            )
            create_order.save()

            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Pedido Confirmado!")
            return redirect('home')
    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prod
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_info": request.POST,
                "billing_form": billing_form
            })

        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_info": request.POST,
                "billing_form": billing_form
            })

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form
        })

    else:
        messages.success(request, "Acesso Negado!")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prod
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Try to get the shipping address or create a new one
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST' and shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, "Endereço de envio atualizado com sucesso!")
            return redirect('checkout')

        return render(request, "payment/checkout.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form
        })
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        if request.method == 'POST' and shipping_form.is_valid():
            # Lidar com envio de convidados, se necessário
            messages.success(request, "Endereço de envio para convidado adicionado!")
            return redirect('checkout')

        return render(request, "payment/checkout.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form
        })

def payment_success(request):
	
	return render(request, 'payment/payment_success.html', {})