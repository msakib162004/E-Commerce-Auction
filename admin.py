from django.contrib import admin
from .models import User, AuctionList, Comment, WatchList, Bid, ClosedAuction
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "email")


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "bid", "description")


class ClosedAuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "close_a_id", "close_u_id")

admin.site.register(User, UserAdmin)
admin.site.register(AuctionList, AuctionAdmin)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(ClosedAuction, ClosedAuctionAdmin)
