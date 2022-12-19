from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_list, Category, bids, comments


def index(request):
    activeListing = auction_list.objects.filter(isActive=True)
    allCategory = Category.objects.all()
    return render(request, "auctions/index.html", {
        "auctionListing" : activeListing,
        "categories": allCategory
    })

def display_category(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListing = auction_list.objects.filter(isActive=True, category=category)
        allCategory = Category.objects.all()
        return render(request, "auctions/index.html", {
            "auctionListing" : activeListing,
            "categories": allCategory
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

def create_listing(request):
        if request.method == "GET":
            allCategory = Category.objects.all()
            return render (request, 'auctions/createListing.html', {
                "categories" : allCategory
            })
        else:
            #GET data from form
            title = request.POST["title"]
            description = request.POST["description"]
            imageUrl = request.POST["imageUrl"]
            price = request.POST["price"]
            category = request.POST["category"]
            #who is the user
            currentUser = request.user
            
            bid = bids(bids=float(price), user=currentUser)
            bid.save()

            categoryData = Category.objects.get(categoryName=category)
            newListing = auction_list(
                title = title,
                description = description,
                imageUrl = imageUrl,
                price = bid, 
                category = categoryData, 
                owner = currentUser
            )

            newListing.save()
            return HttpResponseRedirect(reverse(index))

def auction (request, id):
    Auction = auction_list.objects.get(pk=id)
    isAuctionInWatchList = request.user in Auction.watchList.all()
    allComments = comments.objects.filter(listing=Auction)
    is_owner = request.user.username == Auction.owner.username
    return render(request, "auctions/auction.html", {
        "Auction": Auction,
        "isAuctionIsWatchList": isAuctionInWatchList, 
        "allComments": allComments,
        "is_owner": is_owner
    })

def closeAuction (request, id):
    Auction = auction_list.objects.get(pk=id)
    Auction.isActive = False
    Auction.save()
    isAuctionInWatchList = request.user in Auction.watchList.all()
    allComments = comments.objects.filter(listing=Auction)
    is_owner = request.user.username == Auction.owner.username
    return render(request, "auctions/auction.html", {
        "Auction": Auction,
        "isAuctionIsWatchList": isAuctionInWatchList, 
        "allComments": allComments,
        "is_owner": is_owner,
        "updated": True,
        "message":"congratulation ! your auction is closed"
    })    

def removeWatchListing (request, id):
    listingData = auction_list.objects.get(pk=id)
    curentUser = request.user
    listingData.watchList.remove(curentUser)
    return HttpResponseRedirect(reverse("auctionTitle", args=(id, )))

def addWatchListing (request, id):
    listingData = auction_list.objects.get(pk=id)
    curentUser = request.user
    listingData.watchList.add(curentUser)
    return HttpResponseRedirect(reverse("auctionTitle", args=(id, )))

def displayWatchList (request):
    currentUser = request.user
    listing = currentUser.auctionWatchList.all()
    return render(request, "auctions/displayWatchList.html",{
        "auctionListing": listing 
    })

def addComment(request, id):
    listingData = auction_list.objects.get(pk=id)
    curentUser = request.user
    message = request.POST['newComment']
    newComment = comments(
        author=curentUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("auctionTitle", args=(id, )))

def addBid(request, id):
    newBid = request.POST['newBid']
    Auction = auction_list.objects.get(pk=id)
    isAuctionInWatchList = request.user in Auction.watchList.all()
    allComments = comments.objects.filter(listing=Auction)
    is_owner = request.user.username == Auction.owner.username
    if float(newBid) > Auction.price.bids: 
        updateBids = bids(user=request.user, bids=float(newBid))
        updateBids.save()
        Auction.price = updateBids
        Auction.save()
        return render(request, "auctions/auction.html", {
            "Auction": Auction,
            "message": "bid update successfully",
            "updated": True,
            "isAuctionIsWatchList": isAuctionInWatchList, 
            "allComments": allComments,
            "is_owner": is_owner,
        })
    else:
        return render(request, "auctions/auction.html", {
            "Auction": Auction,
            "message": "bid update failed",
            "updated": False,
            "isAuctionIsWatchList": isAuctionInWatchList, 
            "allComments": allComments,
            "is_owner": is_owner,
        })


    