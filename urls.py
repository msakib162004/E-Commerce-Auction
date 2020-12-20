from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("view", views.view, name="view"),
    path("comment", views.comment, name="comment"),
    path("mypost", views.mypost, name="mypost"),
    path("closedAuction", views.closedAuction, name="closedAuction"),
    path("auctionYouBid", views.auctionYouBid, name="auctionYouBid"),
    path("auctionWin", views.auctionWin, name="auctionWin"),
    path("search", views.search, name="search"),

]
