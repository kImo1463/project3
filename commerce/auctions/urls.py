from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<int:listing_id>', views.listing_view, name='listing'),
    path('closed_auctions/', views.closed_auctions_view, name='closed_auctions'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('category/<str:category_name>/', views.category_view, name='category'),
]

