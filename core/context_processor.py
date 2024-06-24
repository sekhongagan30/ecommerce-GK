from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Count, Min, Max
from django.contrib import messages

def default(request): # this fn is passed in context_processor in Templates in ecomgk.settings.py
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    addresses = Address.objects.filter(user=request.user.id) # get will give the direct object from list, filter will give us the list
    min_max_price= Product.objects.aggregate(min_price=Min("price"), max_price= Max("price"))
    print("ggn 10", min_max_price)
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            wishlist = None
        WishlistCount = wishlist.count()
    else:
        wishlist = {}
        if 'wishlist_data_obj' in request.session:
            wishlist = request.session['wishlist_data_obj']
        WishlistCount = len(wishlist)
    print("ggn 22", WishlistCount)
    return {
        'categories': categories, # if we write this here 'categories', then we don't need to pass it in context of html file
        'vendors': vendors,
        'addresses': addresses,
        'min_max_price': min_max_price,
        'wishlistCount': WishlistCount
    }