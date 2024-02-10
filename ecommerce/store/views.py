from django.shortcuts import render
from .models import *
from .models import Order
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def  store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = items.count()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 , 'shipping':False}
        cartItems=order['get_cart_items']
    products = Product.objects.all()
    context={'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = items.count()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        cartItems=order['get_cart_items']

    context = {'items': items, 'order': order , 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

from django.views.decorators.csrf import csrf_exempt 
@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = items.count()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        cartItems=order['get_cart_items']

    context = {'items': items, 'order': order , 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    # Load the JSON data from the request body
    data = json.loads(request.body)
    
    
    # Extract productId and action from the JSON data
    productId = data.get('productId')
    action = data.get('action')

    # Print the values for debugging purposes
    print('Action:', action)
    print('productId:', productId)

    customer=request.user.customer
    product= Product.objects.get(id=productId)
    order ,created = Order.objects.get_or_create(customer=customer , complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order , product=product)
    if action=='add':
       orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id =datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=Customer , complete = False)
        total = float (data['form']['total'])
        order.transaction_id = transaction_id   

        if total == order.get_cart_total:
           order.complete  = True
        order.save()

        if order.shipping == True:

            ShippingAddress.objects.create(
                custome=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
    return JsonResponse('payment complete', safe=False)