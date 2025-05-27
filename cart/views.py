from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product, Category
from django.http import JsonResponse

def cart_summary(request):
    categories = Category.objects.all()
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'categories': categories})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Retrieve product_id from the AJAX POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, id=product_id)
        
        # Get the Cart instance and add the product
        
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        
        # Optional: you can return the updated cart details or a success message
        # response = JsonResponse({'Product Name: ':product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Retrieve product_id from the AJAX POST data
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        #return redirect('cart_summary')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Retrieve product_id from the AJAX POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        
        
        # Get the Cart instance and add the product
        
        cart.update(product=product_id, quantity=product_qty)
        
        # Optional: you can return the updated cart details or a success message
        # response = JsonResponse({'Product Name: ':product.name})
        response = JsonResponse({'qty': product_qty})
        #return redirect('cart_summary')
        return response

