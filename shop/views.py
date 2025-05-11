import json
from django.shortcuts import render, redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
# import the logging library
import logging
from django.http import HttpResponse, FileResponse
import stripe
from django.conf import settings
from django.urls import reverse
from .utils import generate_receipt_pdf
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/prodView.html', {'product':product[0]})

def payment_confirmation(request):
    payment_intent_id = request.GET.get('payment_intent')
    if not payment_intent_id:
        return HttpResponse("No payment intent provided.", status=400)

    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        order_id = intent.description.split('#')[1]
        order = Orders.objects.get(order_id=order_id)
        amount_pkr = float(intent.amount) / 100 * 280
        amount_usd = float(intent.amount) / 100
        receipt_filename = generate_receipt_pdf(order, amount_pkr, f"${amount_usd:.2f}")
        receipt_path = os.path.join(settings.MEDIA_ROOT, 'receipts', receipt_filename)
        return FileResponse(open(receipt_path, 'rb'), as_attachment=True, filename=receipt_filename)
    except Exception as e:
        logger.error(f"Error in payment confirmation: {str(e)}")
        return HttpResponse(f"Error loading payment confirmation: {str(e)}", status=500)

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        payment_method_id = request.POST.get('payment_method_id', '')

        try:
            # Create the order
            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                          state=state, zip_code=zip_code, phone=phone)
            order.save()

            # Calculate amount in PKR
            amount_pkr = float(request.POST.get('totalPrice', 0))
            
            # Convert PKR to USD (using approximate exchange rate)
            # 1 USD ≈ 280 PKR (you should use a real-time exchange rate in production)
            amount_usd = amount_pkr / 280
            
            # Ensure minimum amount of 50 cents USD
            if amount_usd < 0.50:
                amount_usd = 0.50
                amount_pkr = amount_usd * 280  # Convert back to PKR for display
            
            # Convert to cents for Stripe
            amount_in_cents = int(amount_usd * 100)

            # Get the return URL for payment confirmation
            return_url = request.build_absolute_uri('/shop/payment-confirmation/')

            # Create payment intent with automatic payment methods
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,  # Amount in cents
                currency='usd',  # Changed to USD
                payment_method=payment_method_id,
                confirm=True,
                description=f"Order #{order.order_id}",
                receipt_email=email,
                return_url=return_url,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'
                }
            )

            # Update order status
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed and payment received")
            update.save()

            # Redirect to payment confirmation page
            return redirect(f'/shop/payment-confirmation/?payment_intent={intent.id}')

        except stripe.error.CardError as e:
            # Handle card error
            return render(request, 'shop/checkout.html', {'error': e.error.message})
        except Exception as e:
            # Handle other errors
            logger.error(f"Payment error: {str(e)}")
            return render(request, 'shop/checkout.html', {'error': str(e)})

    return render(request, 'shop/checkout.html', {'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
