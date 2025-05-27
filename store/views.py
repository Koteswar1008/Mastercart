# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

import json
from cart.cart import Cart



def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'home.html', context)

def category(request,cat):
    cat=cat.replace('-',' ')

    try:
        categories = Category.objects.all()
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)

        return render(request, 'category.html', {'products':products,'categories': categories, 'category':category})
    except:
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'product.html', {'product':product, 'categories': categories})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})

def login_user(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If the user is valid, log them in
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)

            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.success(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html', {'categories': categories})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def signup_user(request):
    categories = Category.objects.all()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Save the new user
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request,user)

            messages.success(request, 'Registration successful! Fill your details.')
            return redirect('update_info')  # Redirect to the home
        else:
            messages.error(request, 'Registration failed, Try again.')
            return redirect('signup')
    else:
        form = SignUpForm()  # Create a new empty form instance
    return render(request, 'signup.html', {'form':form, 'categories': categories})

def update_user(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User has been updated.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'categories': categories})
    else:
        messages.success(request, 'You must be logged in to access this page.')
        return redirect('home')
    
def update_info(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user=request.user)

        # Handle potential absence of ShippingAddress
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        # Check if both forms are valid before saving
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'Your info has been updated.')
            return redirect('home')
        
        # Render the form with errors if not valid
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form, 'categories': categories})
    else:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')