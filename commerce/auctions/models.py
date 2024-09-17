from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    Start_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def close_auction(self):
        self.is_active = False
        self.save()

    def highest_bidder(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            return highest_bid.bidder
        return None

    def current_price(self):
        if self.current_bid:
            return self.current_bid
        return self.starting_bid


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.amount}"


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"