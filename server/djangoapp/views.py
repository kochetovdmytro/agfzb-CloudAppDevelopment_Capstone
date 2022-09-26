from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html')
    else:
        return render(request, 'djangoapp/index.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # <HINT> Get user information from request.POST
        # <HINT> username, first_name, last_name, password
        username, password, first_name, last_name = request.POST['username'], request.POST['password'], request.POST['first_name'], request.POST['last_name']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'onlinecourse/registration.html', context)


# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5d65d89d-ae87-46c5-a7b2-bc7f377af4e8/dealership-package/getall_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # Return a list of dealer short name
        context = {'dealerships': dealerships}
        print(context)
        return render(request, 'djangoapp/index.html', context)# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5d65d89d-ae87-46c5-a7b2-bc7f377af4e8/dealership-package/get_review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        context['reviews'] = reviews
        context['dealerId'] = dealer_id
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealerId=dealer_id)
        return render(request, 'djangoapp/add_review.html', {'dealerId':dealer_id, 'cars':cars})
    else:
        if request.user.is_authenticated:
            print(request.POST)
            review = {
                "name":request.POST["name"],
                "review":request.POST["review"],
                "purchase_date":request.POST["purchase_date"],
                "dealership":dealer_id
            }
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            review['year'] = None
            review['car_model'] = None
            review['car_make'] = None
            review['purchase_date'] = None

            if review["purchase"]:
                car = CarModel.objects.filter(id=int(request.POST['car']))
                review['year'] = car.year
                review['car_model'] = car.name
                review['car_make'] = car.car_make
                review['purchase_date'] = request.POST['purchase_date']
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/5d65d89d-ae87-46c5-a7b2-bc7f377af4e8/dealership-package/post-review"
            json_payload = {'review' : review}
            response = post_request(url, json_payload)
            print(response)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return HttpResponse('Authenticate first')


