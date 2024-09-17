
from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, Watchlist

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_bid', 'current_bid', 'is_active', 'created_at', 'Start_time')
    search_fields = ('title', 'description', 'owner__username', 'category')
    list_filter = ('is_active', 'category', 'created_at', 'Start_time')

class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'listing', 'amount', 'bid_time')
    search_fields = ('bidder__username', 'listing__title')
    list_filter = ('bid_time',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'content', 'created_at')
    search_fields = ('user__username', 'listing__title', 'content')
    list_filter = ('created_at',)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    search_fields = ('user__username', 'listing__title')

admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)