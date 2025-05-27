from django.shortcuts import render, redirect
from store.models import Category, Product
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages

def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        my_shipping = request.session.get('my_shipping', None)
        
        
        # Get user data
        full_name = my_shipping.get('shipping_full_name', '')
        email = my_shipping.get('shipping_email', '')
        shipping_address = f"{my_shipping.get('shipping_address1', '')}\n{my_shipping.get('shipping_address2', '')}\n{my_shipping.get('shipping_city', '')}\n{my_shipping.get('shipping_state', '')}\n{my_shipping.get('shipping_country', '')}"
        amount_paid = totals
        user = request.user if request.user.is_authenticated else None

        # Create and save the order
        create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
        create_order.save()

        # Create OrderItems and link them to the created order
        for product in cart_products:
            price = product.sale_price if product.is_sale else product.price
            quantity = quantities.get(str(product.id), 1)
            OrderItem.objects.create(
                order=create_order,  # Set the order directly instead of order_id
                product=product,
                user=user,
                quantity=quantity,
                price=price
            )

        messages.success(request, "Order Placed!")
        return redirect('home')
    else:
        messages.error(request, "Access denied.")
        return redirect('home')

def billing_info(request):
    if request.POST:

        categories = Category.objects.all()
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()


        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_info':request.POST, 'billing_form':billing_form, 'categories': categories})
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_info':request.POST, 'billing_form':billing_form, 'categories': categories})


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, 'shipping_form':shipping_form, 'categories': categories})
    else:
        messages.success(request, "Access denied.")
        return redirect('home')


def checkout(request):
    categories = Category.objects.all()
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Get or create the ShippingAddress for the user
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        
        # Initialize the ShippingForm with the existing or newly created instance
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # If the user is not authenticated, initialize an empty form
        shipping_form = ShippingForm(request.POST or None)

    # Render the checkout page with necessary context
    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
        "categories": categories,
    })


def payment_success(request):
    return render(request, "payment/payment_success.html", {})