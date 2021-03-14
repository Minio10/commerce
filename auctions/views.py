from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment

class NewListingForm(forms.Form):

        title = forms.CharField(label = "Title",widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        ))
        desc = forms.CharField(label = "Description",widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        ))
        init_bid = forms.IntegerField(label = "Initial Price",widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        ))
        url = forms.CharField(label = "Listing Image URL",widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        ))
        category = forms.CharField(label ="Category",widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        ))




def index(request):

    # Returns all listings stored on the DB
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#Sends the user to the page where he can create a new Listing
def create(request):

    return render(request,"auctions/create_listing.html",{
        "form":NewListingForm()
    })

def add_listing(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)

        # Verifies if the form is filled in the correct way
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["desc"]
            init_bid = form.cleaned_data["init_bid"]
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]

        #Adds the Listing to the DB
        new_listing = Listing()
        new_listing.user = request.user
        new_listing.title = title
        new_listing.description = desc
        new_listing.category = category
        new_listing.image_link = url
        new_listing.start_value = init_bid
        new_listing.save()

        #Redirects the user to the Index Template
        return HttpResponseRedirect(reverse("index"))
