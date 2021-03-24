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
    path("close_auction/<int:item_id>",views.close_auction,name = "close_auction"),
    path("watchlist",views.watchlist, name = "watchlist"),
    path("add_watchlist/<int:item_id>",views.add_watchlist,name = "add_watchlist"),
    path("remove_watchlist/<int:item_id>",views.remove_watchlist,name = "remove_watchlist"),
    path("addComment",views.addComment,name = "addComment"),
    path("categories",views.categories,name ="categories"),
    path("viewListingCategories/<str:category>",views.viewListingCategories,name = "viewListingCategories")
]
