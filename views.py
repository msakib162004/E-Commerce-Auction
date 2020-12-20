from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionList, Comment, WatchList, Bid, ClosedAuction


def index(request):
    close_auction = ClosedAuction.objects.all()
    close_a = []
    user_login = 0
    for close in close_auction:
        close_a.append(close.close_a_id)
    current_user = request.user
    if current_user.id:
        user_login = 1
    else:
        user_login = 0
    return render(request, "auctions/index.html", {
        "auctionList": AuctionList.objects.all(),
        "close_auction": ClosedAuction.objects.all(),
        "close_a": close_a,
        "user_login": user_login,
        "bids": Bid.objects.all(),

    })


def closedAuction(request):
    close_auction = ClosedAuction.objects.all()
    close_a = []

    for close in close_auction:
        close_a.append(close.close_a_id)

    return render(request, "auctions/closedAuction.html", {
        "auctionList": AuctionList.objects.all(),
        "close_auction": ClosedAuction.objects.all(),
        "close_a": close_a,
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


def newEntry(request):
    if request.method == "POST":
        current_user = request.user
        entry = AuctionList()
        entry.title = request.POST["title"]
        entry.description = request.POST["description"]
        entry.bid = request.POST["bid"]
        entry.image = request.POST["image"]
        entry.category = request.POST["category"]
        entry.author = current_user
        entry.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/newEntry.html")


def watchlist(request):
    current_user = request.user
    if request.method == "POST":
        watchList_id = int(request.POST["watchlist_id"])
        instance = WatchList.objects.get(id=watchList_id)
        instance.delete()
        return render(request, "auctions/watchlist.html", {
            "user_id": current_user.id,
            "watchList": WatchList.objects.all(),
            "auctions": AuctionList.objects.all(),

        })
    return render(request, "auctions/watchlist.html", {
        "user_id": current_user.id,
        "watchList": WatchList.objects.all(),
        "auctions": AuctionList.objects.all(),

    })


def view(request):
    current_user = request.user
    if request.method == "POST":
        current_auction = int(request.POST["current_auction"])
        close_auction = ClosedAuction.objects.all()
        bid = Bid.objects.all()
        flag = ''
        temp = 0
        temp1 = 0
        for close in close_auction:
            if current_auction == close.close_a_id:
                temp = 1
        for b in bid:
            if b.bid_a_id == current_auction:
                flag = b.id
                temp1 = 1
        if flag:
            return render(request, "auctions/view.html", {
                "id": current_auction,
                "auctions": AuctionList.objects.all(),
                "comment": Comment.objects.all(),
                "show_error": 1,
                "bids": Bid.objects.get(pk=flag),
                "closed_auction": temp,
                "current_user": current_user,
                "temp1": temp1,
            })
        else:
            return render(request, "auctions/view.html", {
                "id": current_auction,
                "auctions": AuctionList.objects.all(),
                "comment": Comment.objects.all(),
                "closed_auction": temp,
                "current_user": current_user,
                "temp1": temp1,
            })


def comment(request):
    if request.method == "POST":
        if request.POST.get('comment'):
            com = request.POST.get('comment')
            id = int(request.POST.get('id'))
            reply = Comment()
            reply.comment = com
            current_user = request.user
            reply.author = current_user
            reply.auction = AuctionList.objects.get(pk=id)
            reply.save()
            bid = Bid.objects.all()
            flag = ''
            for b in bid:
                if b.bid_a_id == id:
                    flag = b.id
            if flag:
                return render(request, "auctions/view.html", {
                    "id": id,
                    "auctions": AuctionList.objects.all(),
                    "comment": Comment.objects.all(),
                    "show_error": 1,
                    "bids": Bid.objects.get(pk=flag),
                    "closed_auction": 0,

                })
            else:
                return render(request, "auctions/view.html", {
                    "id": id,
                    "auctions": AuctionList.objects.all(),
                    "comment": Comment.objects.all(),
                    "closed_auction": 0,
                })
        elif request.POST.get('watchlist_auction'):
            watchlist_auction = request.POST.get('watchlist_auction')
            w_list = WatchList()
            w_list.auction_id = int(watchlist_auction)
            current_user = request.user
            w_list.user = current_user
            w_list.save()
            bid = Bid.objects.all()
            flag = ''
            for b in bid:
                if b.bid_a_id == int(watchlist_auction):
                    flag = b.id
            if flag:
                return render(request, "auctions/view.html", {
                    "id": int(watchlist_auction),
                    "auctions": AuctionList.objects.all(),
                    "comment": Comment.objects.all(),
                    "show_error": 1,
                    "bids": Bid.objects.get(pk=flag),
                    "closed_auction": 0,
                })
            else:
                return render(request, "auctions/view.html", {
                    "id": int(watchlist_auction),
                    "auctions": AuctionList.objects.all(),
                    "comment": Comment.objects.all(),
                    "closed_auction": 0,
                })

        elif request.POST.get('bid'):
            n_bid = float(request.POST.get('bid'))
            watchlist_auction = int(request.POST.get('a_id'))
            current_user = request.user
            bid = Bid.objects.all()
            auction = AuctionList.objects.get(pk=watchlist_auction)
            show_error = 1
            temp = True
            bid_id = ''
            c_bid = 0
            if bid:
                for b in bid:
                    if b.bid_a_id == watchlist_auction:
                        c_bid = 1
                        if b.bid < n_bid:
                            b.bid = n_bid
                            b.bid_user = current_user
                            bid_id = b.id
                            b.save()
                        else:
                            show_error = 0
                        temp = False
            if temp:
                    if auction.bid < n_bid:
                        flag = Bid()
                        flag.bid = n_bid
                        flag.bid_a_id = watchlist_auction
                        flag.bid_user = current_user
                        flag.save()
                        bid_id = flag.id
                    else:
                        show_error = 0
            if show_error == 1:
                return render(request, "auctions/view.html", {
                    "id": watchlist_auction,
                    "auctions": AuctionList.objects.all(),
                    "comment": Comment.objects.all(),
                    "show_error": show_error,
                    "bids": Bid.objects.get(pk=bid_id),
                    "closed_auction": 0,
                    "c_bid": c_bid,
                })
            else:
                if c_bid == 1:
                    return render(request, "auctions/view.html", {
                        "id": watchlist_auction,
                        "auctions": AuctionList.objects.all(),
                        "comment": Comment.objects.all(),
                        "show_error": show_error,
                        "closed_auction": 0,
                        "c_bid": c_bid,
                        "bids": Bid.objects.get(bid_a_id=watchlist_auction),
                    })
                else:
                    return render(request, "auctions/view.html", {
                        "id": watchlist_auction,
                        "auctions": AuctionList.objects.all(),
                        "comment": Comment.objects.all(),
                        "show_error": show_error,
                        "closed_auction": 0,
                        "c_bid": c_bid,
                    })


def mypost(request):
    current_user = request.user
    close_bid = 1
    if request.method == "POST":
        if request.POST.get('current_auction'):
            current_auction = int(request.POST.get('current_auction'))
            closeauctons = ClosedAuction.objects.all()
            for closeauction in closeauctons:
                if current_auction == closeauction.close_a_id:
                    close_bid = 0
            try:
                print("1")
                return render(request, "auctions/mypost.html", {
                    "auction": AuctionList.objects.get(pk=current_auction),
                    "comment": Comment.objects.all(),
                    "id": current_auction,
                    "bids": Bid.objects.get(bid_a_id=current_auction),
                    "flag": 1,
                    "current_price": 1,
                    "close_bid": close_bid,
                    "current_user": current_user,
                })
            except:
                print("2")
                return render(request, "auctions/mypost.html", {
                    "auction": AuctionList.objects.get(pk=current_auction),
                    "comment": Comment.objects.all(),
                    "id": current_auction,
                    "flag": 1,
                    "current_price": 0,
                    "close_bid": close_bid,
                    "current_user": current_user,
                })
        if request.POST.get('id'):
            print("here")
            id = int(request.POST.get('id'))

            try:
                print("3")
                bid = Bid.objects.get(bid_a_id=id)
                closeauction = ClosedAuction()
                closeauction.close_a_id = id
                closeauction.close_u_id = bid.bid_user.id
                closeauction.save()
                return render(request, "auctions/mypost.html", {
                    "auction": AuctionList.objects.get(pk=id),
                    "comment": Comment.objects.all(),
                    "id": id,
                    "bids": Bid.objects.get(bid_a_id=id),
                    "flag": 1,
                    "current_price": 1,
                    "close_bid": 0,
                    "current_user": current_user,
                })
            except:
                print("4")
                closeauction = ClosedAuction()
                closeauction.close_a_id = id
                closeauction.close_u_id = 0
                closeauction.save()
                return render(request, "auctions/mypost.html", {
                    "auction": AuctionList.objects.get(pk=id),
                    "comment": Comment.objects.all(),
                    "id": id,
                    #"bids": Bid.objects.get(bid_a_id=id),
                    "flag": 1,
                    "current_price": 1,
                    "close_bid": 0,
                    "current_user": current_user,
                })

    return render(request, "auctions/mypost.html", {
        "user_id": current_user.id,
        "auctions": AuctionList.objects.all(),
        "flag": 0
    })


def auctionYouBid(request):
    current_user = request.user
    you_bid = []
    bids = Bid.objects.all()
    for bid in bids:
        if bid.bid_user.id == current_user.id:
            you_bid.append(bid.bid_a_id)
    return render(request, "auctions/auctionYouBid.html", {
        "you_bid": you_bid,
        "auctions": AuctionList.objects.all(),
    })


def auctionWin(request):
    current_user = request.user
    closed_auction = ClosedAuction.objects.all()
    id = []
    for closed in closed_auction:
        if closed.close_u_id == current_user.id:
           id.append(closed.close_a_id)
    print(current_user.id)
    return render(request, "auctions/auctionwin.html", {
        "auctions": AuctionList.objects.all(),
        "id": id,
    })


def search(request):
    if request.method == "POST":
        search_auction = request.POST["search"]
        search_auction = search_auction.lower()
        auctions = AuctionList.objects.all()
        close_a = ClosedAuction.objects.all()
        a_list = []
        c_list = []
        empty = 1
        for close in close_a:
            c_list.append(close.close_a_id)
        for auction in auctions:
            if auction.category.lower() == search_auction:
                if auction.id not in c_list:
                    a_list.append(auction.id)
        if a_list:
            empty = 0
        else:
            empty = 1
        return render(request, "auctions/search.html", {
            "auctions": auctions,
            "a_list": a_list,
            "empty": int(empty),
            "search": search_auction,
        })
