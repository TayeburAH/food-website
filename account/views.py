from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from .models import *
from order.models import OrderPlaced
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def main(request):
    context = {}
    return render(request, 'main.html', context)


def signup(request):
    if request.user.is_authenticated:  # always check whether logged in or not
        return redirect('home')
    else:
        form = CustomerForm()

        if request.method == 'POST':
            form = CustomerForm(request.POST or None)  # Pass in the data for validation
            if form.is_valid():  # to check and show form.errors in templates
                form.save()
                messages.success(request,
                                 'Account created.')  # we dont have to pass it in, message is sent to all templates
                request.session['Total_quantity'] = 0
                return redirect('login_process')

        context = {'form': form}
        return render(request, 'account/signup.html', context)


# make a login form, pass messages
# Name the input name = "email", name = "password"
def login_process(request):
    # Used HTML Raw Form
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                try:
                    customer = request.user.customer
                    orderplaced = OrderPlaced.objects.get(customer=customer, status='Not confirmed')
                    request.session['Total_quantity'] = orderplaced.total_quantity
                except ObjectDoesNotExist:
                    request.session['Total_quantity'] = 0

                return redirect('main')
            else:
                messages.error(request, 'User or password incorrect.')



    context = {}  # no need to pass any form
    return render(request, 'account/login.html', context)


def logout_process(request):
    customer =request.user.customer  # no need to use this
    # Create First order or get it
    try:
        orderplaced = OrderPlaced.objects.get(customer=customer, status='Not confirmed')
        orderplaced.total_quantity = request.session.get('Total_quantity')
        orderplaced.save()
    except ObjectDoesNotExist:
        pass
    logout(request)
    return redirect('login_process')


def edit_profile(request):
    if request.method == 'GET':                                           #
        request.session['from'] = request.META.get('HTTP_REFERER', '/')   #  when post is recived ,the functions again runs from the top
    customer = get_object_or_404(Customer, user=request.user)             #
    form = CustomerUpdateForm(instance=customer or None)
    if request.method == 'POST':  #  request.META.get('HTTP_REFERER', '/') changes when post request is made
        form = CustomerUpdateForm(request.POST or None,instance=customer or None)
        if form.is_valid():                     # to check and show form.errors in templates
            customer = form.save(commit=False)
            customer.user = request.user  # this is missing from form, so i have to save it
            # here as i need request.user which i cant get in super(Customer,self).save(commit=False)
            customer.address = form.cleaned_data.get('address')
            # since I redesigned the address field, I need to personally
            # save it
            customer.save()
            messages.success(request,'Account updated.')  # we don't have to pass it in, message is sent to all templates
            return redirect(request.session['from'])

    context = {'form': form}
    return render(request, 'account/edit_profile.html', context)


def delete_process(request):
    if request.method == 'POST':

        user = authenticate(request, email=request.user.email, password=request.POST.get('password'))
        if user is not None:
            user.delete()
            return redirect('home')
        else:
            messages.error(request, 'password incorrect')

    context = {}  # no need to pass any form
    return render(request, 'account/delete_process.html', context)


# AJAX
def load_cities(request):
    division_id = request.GET.get('division_id')

    cities = City.objects.filter(division_id=division_id)
    # return render(request, 'persons/city_dropdown_list_options.html', {'cities': cities})
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


# AJAX
def load_zips(request):
    city_id = request.GET.get('city_id')
    zips = Zip.objects.filter(city_id=city_id)
    # return render(request, 'persons/city_dropdown_list_options.html', {'zips': zips})

    return JsonResponse(list(zips.values('id', 'name')), safe=False)
