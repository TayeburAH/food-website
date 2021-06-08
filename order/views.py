from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from food.models import Product
from account.models import Customer
from django.contrib.auth import get_user_model
from datetime import datetime

from django.contrib.auth.decorators import login_required

from django.conf import settings

User = get_user_model()


# Create your views here.

# def add_to_cart(request):
#     result = {'status': 'ok'}
#     if request.method == 'GET':
#         if not (request.GET.get("price") and request.GET.get("product_id")):
#             result = {'status': '404'}
#             return JsonResponse(result)
#         else:
#             product_id = request.GET.get("product_id")
#             size = request.GET.get("size")
#             product = Product.objects.get(id=product_id)
#             price = request.GET.get("price")
#
#
#             # Find this specific customer
#             customer = request.user.customer  # OneToOne relation
#             # or use customer = Customer.objects.get(user=request.user)
#             # Create First order or get it
#
#             # Importance of created in get_or_create
#             # foo = Foo.objects.get_or_create(some_attribute='something')  # foo is actually a tuple...
#             # Bar.objects.get_or_create(foo=foo)  # this will raise the error
#
#             orderplaced, created = OrderPlaced.objects.get_or_create(customer=customer, status='Not confirmed')
#             # use get_or_create to update cart items
#             obj, created = CartItems.objects.get_or_create(orderplaced=orderplaced, product=product, size=size,
#                                                            price=price)
#             if not created:
#                 obj.quantity += 1
#                 if obj.quantity <= 5:
#                     obj.save()
#                 else:
#                     result['limit'] = 'True'
#                     return JsonResponse(result)
#             else:
#                 obj.sub_total = price
#                 obj.save()
#             return JsonResponse(result)

@login_required(login_url="/login_page")
def cart_operation(request):
    result = {'status': 'ok'}
    if request.method == 'GET':
        product_id = request.GET.get("product_id")
        size = request.GET.get("size")
        price = request.GET.get("price")
        operation = request.GET.get("operation")
        customer = Customer.objects.get(user=request.user)  # no need to use this
        # Create First order or get it
        orderplaced, created = OrderPlaced.objects.get_or_create(customer=customer, status='Not confirmed')
        product = Product.objects.get(id=product_id)
        # use get_or_create to update cart items
        obj, created = CartItems.objects.get_or_create(orderplaced=orderplaced, product=product, size=size,
                                                       price=price)

        # You need these values, you need to get them by jquery from .val, .attr from html
        # product_id = request.GET.get("product_id")
        # size = request.GET.get("size")
        # price = request.GET.get("price")
        # operation = request.GET.get("operation")
        if not created:
            if operation == 'add' or operation == 'add_to_cart':
                if obj.quantity < 5:
                    obj.quantity += 1
                    obj.save()
                    print('Created', obj.quantity)
                else:
                    result['limit'] = 'True'

            if operation == 'sub':
                if obj.quantity > 1:
                    obj.quantity -= 1
                    obj.save()
                else:
                    obj.delete()
                    result['delete'] = 'True'

            if operation == 'remove':
                obj.delete()
                result['delete'] = 'True'
                # del request.session['Total_quantity']

            # the change in calculations, saving, json
            result['sub_total'] = obj.sub_total
            result['quantity'] = obj.quantity
            items = orderplaced.cartitems_set.all()
            sum_of_cart_items = sum([item.quantity * item.price for item in items])
            Quantity = sum([item.quantity for item in items])
            request.session['Total_quantity'] = Quantity
            result['sum_of_cart_items'] = sum_of_cart_items
            result['Quantity'] = Quantity
            return JsonResponse(result)
        else:
            print('first time', obj.quantity)
            obj.save()
            # for total cart items
            items = orderplaced.cartitems_set.all()
            Quantity = sum([item.quantity for item in items])
            request.session['Total_quantity'] = Quantity
            result['Quantity'] = Quantity
            return JsonResponse(result)

            # cart = request.session.get('cart')
            # if cart:
            #     if product_id in cart:
            #         if size in cart[product_id]['size']:
            #             cart[product_id]['quantity'] += 1
            #
            #         else:
            #             cart[product_id] = {
            #                 'quantity': 1,
            #                 'size': size,
            #                 'price': price,
            #             }
            #
            #
            #     else:
            #         cart[product_id] = {
            #             'quantity': 1,
            #             'size': size,
            #             'price': price,
            #         }
            # else:
            #     cart = {product_id: {
            #         'quantity': 1,
            #         'size': size,
            #         'price': price,
            #     }}  # request.session= {  cart:{}   }
            #
            # # Save new data in request.session= {  cart:{}   }
            # request.session['cart'] = cart  # request.session= {  cart:{}   }    = cart[product_id]
            # print(request.session.get('cart'))
            #
            #
            # # request.session['Total_quantity'] = cart['quantity']
            # # result['Quantity'] = cart['quantity']
            # return JsonResponse(result)


# def minus_cart(request):
#     result = {'status': 'ok'}
#     if request.method == 'GET':
#         if not (request.GET.get("price") and request.GET.get("product_id") and request.GET.get("size")):
#             result = {'status': '404'}
#             return JsonResponse(result)
#         else:
#             product_id = request.GET.get("product_id")
#             size = request.GET.get("size")
#             product = Product.objects.get(id=product_id)
#             price = request.GET.get("price")
#
#             customer = Customer.objects.get(user=request.user)
#             # Create First order or get it
#             orderplaced, created = OrderPlaced.objects.get_or_create(customer=customer, status='Not confirmed')
#             # use get_or_create to update cart items
#             obj, created = CartItems.objects.get_or_create(orderplaced=orderplaced, product=product, size=size,
#                                                            price=price)
#             if not created:
#
#                 obj.quantity -= 1
#                 if obj.quantity > 0:
#                     obj.save()
#                     result['sub_total'] = obj.sub_total
#                     result['quantity'] = obj.quantity
#                     items = orderplaced.cartitems_set.all()
#                     sum_of_cart_items = sum([item.quantity * item.price for item in items])
#                     result['sum_of_cart_items'] = sum_of_cart_items
#                     return JsonResponse(result)
#                 else:
#                     result['limit'] = 'True'
#
#                     return JsonResponse(result)
#
#             else:
#                 obj.sub_total = price
#                 obj.save()
#             return JsonResponse(result)
#
#
# def remove_cart(request):
#     result = {'status': 'ok'}
#     if request.method == 'GET':
#         if not (request.GET.get("product_id") and request.GET.get("price")):
#             result = {'status': '404'}
#             return JsonResponse(result)
#         else:
#             price = request.GET.get("price")
#             product_id = request.GET.get("product_id")
#
#             customer = Customer.objects.get(user=request.user)
#             # Create First order or get it
#
#             orderplaced = OrderPlaced.objects.get(Q(customer=customer) & Q(status='Not confirmed'))
#             obj = CartItems.objects.get(Q(orderplaced=orderplaced) & Q(product=product_id) & Q(price=price))
#             obj.delete()
#             items = orderplaced.cartitems_set.all()
#             sum_of_cart_items = sum([item.quantity * item.price for item in items])
#             result['sum_of_cart_items'] = sum_of_cart_items
#             result['delete'] = 'True'
#             return JsonResponse(result)

@login_required(login_url="/login_page")
def cart(request):
    # items = CartItems.objects.filter(user=request.user) # works fine
    # orderplaced, created = OrderPlaced.objects.get_or_create(customer=request.user.customer, status='Not confirmed')
    # Any field  username= request.user.username although __str__ returns username
    try:
        customer = request.user.customer
        orderplaced = OrderPlaced.objects.get(customer=customer, status='Not confirmed')
        items = orderplaced.cartitems_set.all()
    except ObjectDoesNotExist:
        return render(request, 'empty_cart.html')

    if items:
        sum_of_cart_items = sum([item.quantity * item.price for item in items])

        context = {
            'items': items,
            'sum_of_cart_items': sum_of_cart_items,

        }
        return render(request, 'cart.html', context)
    else:
        return render(request, 'empty_cart.html')


@login_required(login_url="/login_page")
def checkout(request):
    try:
        customer = request.user.customer
        orderplaced = OrderPlaced.objects.get(Q(customer=customer) & Q(status='Not confirmed'))
        items = orderplaced.cartitems_set.all()
    except:
        return redirect('/cart')

    sum_of_cart_items = sum([item.quantity * item.price for item in items])
    # Address
    customer = Customer.objects.get(user_id=request.user.id)
    shipping_charge = 4
    context = {
        'items': items,
        'sum_of_cart_items': sum_of_cart_items,
        'customer': customer,
        'shipping_charge': orderplaced.shipping_cost,
        'id': orderplaced.pk,
    }

    return render(request, 'checkout.html', context)


@login_required(login_url="/login_page")
def order_tracker(request):
    try:
        if request.method == 'POST':
            cash = request.POST.get('Cash')
            id = request.POST.get('order_id')
            orderplaced = OrderPlaced.objects.get(pk=id)
            orderplaced.status = 'Processing'
            orderplaced.order_date = datetime.now()
            orderplaced.cash = cash
            orderplaced.save()
            request.session['Total_quantity'] = 0
    except ObjectDoesNotExist:
        return redirect('/home')

    # Show all orders on order_status.html
    customer = request.user.customer
    orderplaced = OrderPlaced.objects.filter(customer=customer).filter(~Q(status__in=['Not confirmed'])).order_by(
        '-order_date')

    if orderplaced:
        context = {
            'active_link': 'order_summary',
            'orderplaced': orderplaced,
        }
        return render(request, 'order_status.html', context)

    else:
        return render(request, 'no_order_status.html')
