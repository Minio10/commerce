from django.urls import path
from .models import Listing

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name ="create"),
    path("add_listing",views.add_listing,name ="add_listing"),
    path("listing/<int:pk>",views.viewListing, name ="viewListing"),
    path("place_bid",views.placeBid,name = "placeBid"),
    path("close_auction/<int:item_id>",views.close_auction,name = "close_auction")
]
