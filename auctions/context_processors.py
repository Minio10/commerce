from .models import User, Listing, Bid, Comment, Watchlist



def sections_processor(request):
    # do something ...
    if request.user.is_authenticated:
        num = Watchlist.objects.filter(user = request.user).count()
        if not num:
            return {'NumItems':0}

        return {'NumItems': num}

    return {'NumItems':''}
