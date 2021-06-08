from django.db.models import Q
from django.shortcuts import render
from .models import *


# Create your views here.


def home(request):
    context = {
        'active_link': 'home'
    }
    return render(request, 'food/home.html', context)


def pizza(request):
    category = Category.objects.get(name='pizza')
    pizza = Product.objects.filter(category=category)
    context = {
        'active_link': 'pizza',
        'products': pizza
    }
    return render(request, 'food/pizza.html', context)


def burger(request):
    category = Category.objects.get(name='burger')
    burger = Product.objects.filter(category=category)
    context = {
        'active_link': 'burger',
        'products': burger,
    }
    return render(request, 'food/burger.html', context)


def fried_chicken(request):
    category = Category.objects.get(name='chicken')
    chicken = Product.objects.filter(category=category) # send a QuerySet, <QuerySet [<Product: Curly Fries>, <Product: Crinkle Cut Fries>, <Product: Shoestring Fries>, <Product: Chilli Cheese Fries>]>

    context = {
        'active_link': 'fried_chicken',
        'products': chicken,
    }
    return render(request, 'food/burger.html', context)


def french_fries(request):
    category = Category.objects.get(name='french_fry')
    fry = Product.objects.filter(category=category)
    print(fry)
    fries=[]  # send a list
    for fry in fry:
        fries.append(fry)
    context = {
        'active_link': 'french_fries',
        'products': fries,
    }
    return render(request, 'food/burger.html', context)


def search(request):
    products = []
    q = request.GET.get('q').split(' ')
    print(q[0])

    # categories = [categories.name  for categories in  Category.objects.all()]
    # print(categories)
    product = Product.objects.filter(name__icontains=q[0])
    print(product)

    for q in q:
        searched_product = Product.objects.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q)
        ).distinct()

        for product in searched_product: # to remove QuerySet
            products.append(product)

    print(products) # working
    print(list(set(products)))  # set to remove same items,than list them
    context = {
        'products': products,
    }
    return render(request, 'food/search.html', context)