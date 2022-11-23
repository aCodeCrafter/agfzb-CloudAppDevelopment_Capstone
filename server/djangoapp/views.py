from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel
# from .restapis import related methods
from .restapis import get_request, post_request, get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def render_generic_static_page(request):
    context = {}
    if request.method == "GET":
        return render(request,'car_dealership/index.html',context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request,'djangoapp/about.html',context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request,'djangoapp/contact.html',context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        user = authenticate(request,
        username=request.POST['username'],
        password=request.POST['password'])

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print('Failed to authenticate user')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/djangoapp/')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        User.objects.create_user(username=request.POST['username'],
                                first_name=request.POST['firstname'],
                                last_name=request.POST['lastname'],
                                password=request.POST['password'])
        login(request, authenticate(request,
                                    username=request.POST['username'],
                                    password=request.POST['password']))
        return HttpResponseRedirect('/djangoapp/')
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/aCodeCrafter%40gmail.com_dev/dealership-package/dealership'
        dealerships = get_dealers_from_cf(url)
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a
def get_dealer_details(request, dealer_id):
    print(f'Dealer ID: {dealer_id}')
    context = {}
    if request.method == "GET":
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/aCodeCrafter%40gmail.com_dev/dealership-package/review'
        reviews = get_dealer_reviews_from_cf(url=url,dealer_id=dealer_id)
        if len(reviews) == 0:
            context['display_message'] = "Looks like this dealer Doesn't have any reviews. Be the first to add one!"
        else:
            context['display_message'] = ''
        context['reviews'] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request,dealer_id):
    context = {}
    json_body = {}
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/aCodeCrafter%40gmail.com_dev/dealership-package/review'

    # basic_review = {
    #     'name' : 'Bob Dillan',
    #     'dealership' : 11,
    #     'review' : 'It was an amazing dealership!',
    #     'purchase' : True,
    #     'purchase_date' : '11/03/22',
    #     'car_make' : 'Toyota',
    #     'car_model' : 'Camri',
    #     'car_year' : '2004'
    # }

    if request.method == 'POST':
        if request.user.is_authenticated:
            review = dict()
            review['sentiment'] = analyze_review_sentiments(request.POST['review'])
            review['name'] = request.POST['name']
            review['dealership'] = dealer_id
            review['review'] = request.POST['review']
            if 'purchase' in request.POST.keys():
                review['purchase'] = True
            else:
                review['purchase'] = False
            review['purchase_date'] = request.POST['purchase_date']
            car_obj = CarModel.objects.filter(id=request.POST['car_id']).first()
            review['car_model'] = car_obj.name
            review['car_make'] = car_obj.make.name
            review['car_year'] = int(str(car_obj.year)[:4])


            # print(f'\n\nREVIEW: {review}\n\n')
            json_resp = post_request(url=url, json_payload=review)
            if json_resp['status_code'] == 201:
                # return True
                return redirect("/djangoapp", dealer_id=dealer_id)
            else:
                print(f'An error occured while submitting a review\n Error code: {json_resp["status_code"]}')
                return redirect("/djangoapp", dealer_id=dealer_id)
        else:
            return HttpResponse('Unauthorized', status=401)
    elif request.method == 'GET':
        context['dealer_id'] = dealer_id
        context['cars'] = CarModel.objects.all()
        return render(request,'djangoapp/add_review.html',context)
