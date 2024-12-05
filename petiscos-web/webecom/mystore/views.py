from django.shortcuts import render, redirect
from .models import Products, Categories, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UpdateProfileForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        
        # Query the products in DataBase.
        searched = Products.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        
        if not searched:
            messages.error(request, 'Desculpa, o produto que procuras não está disponivel!!.')
            return render(request, 'search.html', {})    
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
        return render(request, 'search.html', {}) 


def update_profile(request):
    if request.user.is_authenticated:
        # Current User.
        current_user = Profile.objects.get(user__id=request.user.id)
        
        try:
            # Get Current User's Shipping Form.
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            # Se o usuário não tiver um endereço de envio, crie um novo.
            shipping_user = ShippingAddress(user=request.user)

        # Get User Original Form.
        form = UpdateProfileForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            
            messages.success(request, 'A informação do teu perfil foi atualizada com sucesso!')
            return redirect('home')
        
        return render(request, 'update_profile.html', {
            'form': form, 
            'shipping_form': shipping_form
        })
    
    else:
        messages.error(request, 'Tens de ter uma conta para poderes atualizar o teu perfil.')
        return redirect('home')
    
    
# Change the user password View.
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'A tua palavra-chave foi alterada com sucesso!.')
                login(request, current_user)        
                return redirect('update_user')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form}) 
    else:
        messages.error(request, 'Tens de ter uma conta para poderes atualizar o teu perfil.')
        return redirect('home')

# Change the users info View.
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, 'O teu perfil foi atualizado com sucesso!.')
            return redirect('home')
        
        return render(request, 'update_user.html', {'user_form':user_form}) 
    
    else:
        messages.error(request, 'Tens de ter uma conta para poderes atualizar o teu perfil')
        return redirect('home')

# View to list all the categories. (Gonna be removed or updated soon..).
def category_summary(request):
    categories = Categories.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})
    
# View where we obtain the products for each category.
def category(request, cn):
    try:
        category = Categories.objects.get(name=cn)
        products = Products.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products, 
            'category': category
        })
    except Categories.DoesNotExist:
        messages.error(request, 'Desculpa, neste momento não há produtos desta categoria.')
        return redirect('home')
    
# Particular product View.
def product(request,pk):
    product = Products.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

# Home Page View.
def home(request):
    products = Products.objects.all()
    return render(request, 'home.html', {'products':products}) 

def t_about_product(request,pk):
    product = Products.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def t_home(request):
    # Search for 10 products at random for the first page.
    products = Products.objects.all().order_by('?')[:8]
    return render(request, 't_home.html', {'products': products})

# About Us View.
def about(request):
    return render(request, 'about.html', {})

# Login Page View.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Get the user profile.
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get the old_cart string.
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary.
            if saved_cart:
                # Convert to dictionary using JSON.
                converted_cart = json.loads(saved_cart)
                # Add the cart dictionary to the user session.
                cart = Cart(request)
                # Loop through the cart to append the items from our database.
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity= value)
            
            messages.success(request, ('Bem vindo, você entrou na sua conta!.'))
            return redirect('home')
        else: 
            messages.error(request, ('Não conseguiste entrar, talvez tenha havido um problema na escrita?'))
            return redirect('login')
            
    else:
        return render(request, 'login.html', {}) 

# Logout View.
def logout_user(request):
    logout(request)
    messages.success(request, ('Saiste da tua conta com sucesso!'))
    return redirect('home')

# Register View.
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Conta criada com sucesso, podes agora entrar!.'))
            return redirect('update_profile')
        else:
            messages.error(request, ('Alguma coisa aconteceu, mas tens de tentar novamente!'))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})