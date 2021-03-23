from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Watchlist

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

class NewBidForm(forms.Form):

    value = forms.IntegerField(widget = forms.TextInput(
        attrs = {
            'class': 'form-control','placeholder': 'Bid'
        }
    ))
    item_id = forms.IntegerField(widget = forms.HiddenInput())



def index(request):

    # Returns all active listings stored on the DB
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(flag_active = 0)
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

def viewListing(request,pk):


    # returns the listing selected
    listing = Listing.objects.get(id=pk)

    # returns the list of bids made on that specific listing
    bid_List = Bid.objects.filter(item = pk)

    #checks if the item is already on the users watchlist
    watchlist = Watchlist.objects.filter(user = request.user, item = pk)



    return render(request, "auctions/listing.html",{
        "listing":listing,"form":NewBidForm(),"num_bids":len(bid_List),"watchlist":watchlist
    })






def placeBid(request):

    if request.method == "POST":
        form = NewBidForm(request.POST)

        if form.is_valid():
            bid = form.cleaned_data["value"]
            item_id = form.cleaned_data["item_id"]

            listing = Listing.objects.get(id=item_id)

            if(bid > listing.start_value):

                new_bid = Bid()
                new_bid.value = bid
                new_bid.item = listing
                new_bid.user = request.user

                new_bid.save()

                Listing.objects.filter(pk=item_id).update(start_value=bid)

                return redirect("viewListing",item_id)

            else:

                return render(request,"auctions/error.html",{
                    "message": "The value of the bid made is equal or less than the actual price. Please Try again"
                })

def close_auction(request,item_id):

    # returns the listing selected
    listing = Listing.objects.get(id=item_id)

    # returns the list of bids made on that specific listing
    bid_List = Bid.objects.filter(item = item_id)

    # returns the highest bid made on that specific listing
    highest_bid = bid_List.get(value = listing.start_value)

    # This listing is no longer active
    Listing.objects.filter(pk=item_id).update(flag_active=1)

    #Listing Winner
    Listing.objects.filter(pk=item_id).update(winner=highest_bid.user.username)

    return redirect("viewListing",item_id)





def add_watchlist(request,item_id):

    # returns the listing selected
    listing = Listing.objects.get(id=item_id)

    #Verifies if the item already exists on that person's watchlist
    try:
        w_item = Watchlist.objects.get(item = listing, user = request.user)

    except:

        w_item = None

    #If it doesnt exist, its added to the DB
    if not w_item:

        watch_item = Watchlist()
        watch_item.user = request.user
        watch_item.item = listing
        watch_item.save()

        return redirect("viewListing",item_id)

def remove_watchlist(request,item_id):

    # returns the listing selected
    listing = Listing.objects.get(id=item_id)

    #Removing the item from the user's Watchlist
    try:
        w_item = Watchlist.objects.get(item = listing, user = request.user)

    except:

        w_item = None

    w_item.delete()

    return redirect("viewListing",item_id)


def watchlist(request):

    return 0
