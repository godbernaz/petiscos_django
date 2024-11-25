from django.shortcuts import render, redirect
from .models import Products, Categories
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms

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
        return render(request, 'category.html', {'products': products, 'category': category})
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
            return redirect('home')
        else:
            messages.error(request, ('Alguma coisa aconteceu, mas tens de tentar novamente!'))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})