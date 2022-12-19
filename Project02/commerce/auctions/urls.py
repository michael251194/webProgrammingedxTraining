from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing,name="createListing"),
    path("displayCategory", views.display_category,name="displayCategory"),
    path("displayWatchList", views.displayWatchList, name="displayWatchList"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("listing/<int:id>", views.auction, name="auctionTitle"),
    path("removeWatchListing/<int:id>", views.removeWatchListing, name="removeWatchListing"),
    path("addWatchListing/<int:id>", views.addWatchListing, name="addWatchListing"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
]
