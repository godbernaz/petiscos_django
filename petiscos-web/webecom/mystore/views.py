from django.shortcuts import render, redirect
from .models import Products, Categories
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

def category_summary(request):
    categories = Categories.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})
    
    
def category(request, cn):
    try:
        category = Categories.objects.get(name=cn)
        products = Products.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Categories.DoesNotExist:
        messages.error(request, 'Desculpa, neste momento não há produtos desta categoria.')
        return redirect('home')
    
def product(request,pk):
    product = Products.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Products.objects.all()
    return render(request, 'home.html', {'products':products}) 

def about(request):
    return render(request, 'about.html', {})

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

def logout_user(request):
    logout(request)
    messages.success(request, ('Saiste da tua conta!, és sempre bem-vindo novamente!.'))
    return redirect('home')

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