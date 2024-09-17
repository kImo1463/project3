from django.shortcuts import render, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, AuctionListing
from django.utils.dateparse import parse_datetime
from .models import Bid, Comment, Watchlist

def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url", "")
        category = request.POST.get("category", "")
        Start_time = request.POST.get("Start_time")

        Start_time = parse_datetime(Start_time) if Start_time else None

        listing = AuctionListing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_bid=starting_bid,
            owner=request.user,
            image_url=image_url,
            category=category,
            Start_time=Start_time,
        )
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

@login_required
def listing_view(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by('-created_at')
    user_watchlist = request.user.is_authenticated and Watchlist.objects.filter(user=request.user, listing=listing).exists()
    highest_bid = listing.bids.order_by('-amount').first()
    highest_bidder = highest_bid.bidder if highest_bid else None
    error = None

    is_owner = request.user == listing.owner

    if request.method == "POST":
        if 'bid' in request.POST:
            try:
                bid_amount = float(request.POST['bid_amount'])
            except ValueError:
                error = "Invalid bid amount."
            else:
                current_bid = float(listing.current_bid)
                if bid_amount <= current_bid:
                    error = "Your bid must be higher than the current price."
                else:
                    new_bid = Bid(bidder=request.user, listing=listing, amount=bid_amount)
                    new_bid.save()
                    listing.current_bid = bid_amount
                    listing.save()
                    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        elif 'comment' in request.POST:
            comment_content = request.POST['comment_content']
            new_comment = Comment(user=request.user, listing=listing, content=comment_content)
            new_comment.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        elif 'watchlist_add' in request.POST:
            Watchlist.objects.create(user=request.user, listing=listing)
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        elif 'watchlist_remove' in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        elif 'close_auction' in request.POST and is_owner:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        'user_watchlist': user_watchlist,
        'highest_bidder': highest_bidder,
        'error': error,
        'is_owner': is_owner,
        'category': listing.category,
        'listed_by': listing.owner,
    })

@login_required
def closed_auctions_view(request):
    closed_listings = AuctionListing.objects.filter(is_active=False).order_by('-created_at')
    closed_auctions = []

    for listing in closed_listings:
        highest_bid = listing.bids.order_by('-amount').first()
        winner = highest_bid.bidder if highest_bid else None
        closed_auctions.append({
            'listing': listing,
            'winner': winner,
        })

    return render(request, 'auctions/closed_auctions.html', {
        'closed_auctions': closed_auctions,
    })

@login_required
def category_view(request, category_name):
    if category_name == 'all':
        categories = AuctionListing.objects.values_list('category', flat=True).distinct()
        context = {
            "categories": categories,
            "listings_by_category": {}
        }
        for category in categories:
            listings = AuctionListing.objects.filter(is_active=True, category=category)
            context["listings_by_category"][category] = listings
        return render(request, "auctions/categories.html", context)
    else:
        category_listings = AuctionListing.objects.filter(is_active=True, category=category_name)
        return render(request, "auctions/categories.html", {
            "category_name": category_name,
            "listings": category_listings
        })


from django.contrib.auth.decorators import login_required

@login_required
def watchlist_view(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    context = {
        'watchlist': watchlist
    }
    return render(request, 'auctions/watchlist.html', context)
