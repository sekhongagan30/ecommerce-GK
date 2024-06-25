from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from core.models import Product, Category, Vendor, CartOrder, ProductImages, ProductReview, Wishlist, CartData, Address
from userauths.models import Profile
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework  import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class ProductView(APIView):
    http_method_names = ['get']
    renderer_classes = (JSONRenderer,)
    def get(self, request, pid=None):
        if pid is None:
            product = Product.objects.filter(product_status="published")
            context = {
                "products": product
            }
            return render(request, "core/product-list.html", context)
        else:
            product = Product.objects.get(pid=pid)
            # product = get_object_or_404(Product, pid=pid)
            products = Product.objects.filter(category=product.category).exclude(pid=pid)[
                       :4]  # last te dsda k kinne index tk pick krna chonde

            # getting all reviews
            reviews = ProductReview.objects.filter(product=product).order_by("-date")

            # getting average reviews
            # aggregarte fn will add kwargs(rating) as key to the given dict(from filter)
            average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
            # so average_rating= {'ProductReview fieldName':fieldValue , rating: Avg('rating')}
            # just like we normally fetch col by  average_rating.review, we will fetch rating

            # Product review form
            review_forms = ProductReviewForm()

            make_review = True

            if request.user.is_authenticated:
                user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

            p_images = product.p_images.all()
            context = {
                'product': product,
                'p_images': p_images,
                'products': products,
                'reviews': reviews,
                'average_rating': average_rating,
                'review_forms': review_forms
            }
            return render(request, 'core/product-detail.html', context)

class CategoryView(APIView):
    http_method_names = ['get']
    renderer_classes = (JSONRenderer,)
    def get(self, request, cid=None):
        if cid is None:
            category = Category.objects.all()  # .annotate(product_count=Count("product"))
            context = {
                "categories": category
                # this categories in html gives queryset[list of category table rows], {{categories.count}} will give length of category table rows
            }
            return render(request, "core/category-list.html",context)  # in html file, key of context is treated as variable
        else:
            category = Category.objects.get(cid=cid)
            products = Product.objects.filter(product_status="published", category=category)

            context = {
                'category': category,
                'products': products
            }
            return render(request, "core/category-product-list.html", context)

class VendorView(APIView):
    http_method_names = ['get']
    renderer_classes = (JSONRenderer,)
    def get(self, request, vid=None):
        if vid is None:
            vendors = Vendor.objects.all()
            context = {
                'vendors': vendors
            }
            return render(request, 'core/vendor-list.html', context)
        else:
            vendor = Vendor.objects.get(vid=vid)
            products = Product.objects.filter(product_status="published", vendor=vendor)
            context = {
                'vendor': vendor,
                'products': products
            }
            return render(request, 'core/vendor-detail.html', context)

class CartView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']
    renderer_classes = (JSONRenderer,)
    def get(self, request):
        cart_data = {}
        totalCartItems = 0
        cart_total_amount = 0
        if not request.user.is_authenticated:
            if 'cart_data_obj' in request.session:
                for p_id, item in request.session['cart_data_obj'].items():
                    cart_total_amount += int(item['qty']) * float(item['price'])
                cart_data = request.session['cart_data_obj']
                totalCartItems = len(request.session['cart_data_obj'])
        else: # jdo login krega , session cho empty krke db ch insert krna hai
            try:
                cart_data = CartData.objects.filter(user=request.user)
                for data in cart_data:
                    print("ggn 124", data.product.price, (data.qty))
                    amt = float(data.product.price) * (data.qty)
                    cart_total_amount += amt
                print("ggn 125", cart_total_amount)
            except:
                cart_data = None
            totalCartItems = cart_data.count()
            isUserAuthenticated = True
        context = {
            'cart_data': cart_data,
            'totalCartItems': totalCartItems,
            'cart_total_amount': cart_total_amount,
            'isUserAuthenticated': request.user.is_authenticated
        }
        return render(request, "core/cart.html", context)
    def post(self, request):
        cart_product = {}
        if not request.user.is_authenticated:
            productId = str(request.data['pid'])
            cart_product[productId] = {
                'title': request.data['title'],
                'qty': request.data['qty'],
                'price': request.data['price'],
                'image': request.data['image']
            }
            print("ggn 162", request.session, cart_product)
            if 'cart_data_obj' in request.session:
                if productId in request.session['cart_data_obj']:
                    cart_data = request.session['cart_data_obj']
                    cart_data[productId]['qty'] = str(cart_product[productId]['qty'])
                    cart_data.update(cart_data)
                    request.session['cart_data_obj'] = cart_data
                else:
                    cart_data = request.session['cart_data_obj']
                    cart_data.update(cart_product)
                    request.session['cart_data_obj'] = cart_data
            else:
                request.session['cart_data_obj'] = cart_product
            print("ggn 176", request, request.session)
            cartData = request.session['cart_data_obj']
            totalCartItems = len(request.session['cart_data_obj'])
        else:
            productId = str(request.data['pid'])
            qty = request.data['qty']
            product = Product.objects.filter(pid=productId).first()
            c = CartData.objects.filter(product=product, user=request.user)
            print("ggn 170", qty, productId, c)
            totalCartItems = c.count()
            if totalCartItems > 0:
                CartData.objects.filter(product=product, user=request.user).update(qty=qty)
            else:
                new_cartData = CartData.objects.create(
                    product=product,
                    qty = qty,
                    user=request.user,
                )
                print("ggn 179", new_cartData)
            cartData = CartData.objects.filter(user=request.user)
            ##
            totalCartItems = cartData.count()

        context = {
            # 'data': cartData,
            'totalCartItems': totalCartItems
        }
        print("ggn 184", context)
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request):
        error = ""
        cart_total_amount = 0
        product_id = str(request.data['id'])
        qty = request.data['product_qty']
        if not request.user.is_authenticated:
            error = 'Product not present for logged in user !'
            if 'cart_data_obj' in request.session:
                if product_id in request.session['cart_data_obj']:
                    error = ""
                    cart_data = request.session['cart_data_obj']
                    cart_data[product_id]['qty'] = qty
                    request.session['cart_data_obj'] = cart_data

            cart_total_amount = 0
            if 'cart_data_obj' in request.session:
                for p_id, item in request.session['cart_data_obj'].items():
                    cart_total_amount += int(item['qty']) * float(item['price'])
            cart_data = request.session['cart_data_obj']
            totalCartItems = len(request.session['cart_data_obj'])

        else:

            ##
            product = Product.objects.filter(pid=product_id).first()
            c = CartData.objects.filter(product=product, user=request.user)
            totalCartItems = c.count()
            if totalCartItems > 0:
                CartData.objects.filter(product=product, user=request.user).update(qty=qty)
            else:
                error = 'Product not present for logged in user !'
            cart_data = CartData.objects.filter(user=request.user)
            for data in cart_data:
                amt = float(data.product.price) * (data.qty)
                cart_total_amount += amt
            totalCartItems = cart_data.count()
            ##

        context = {
            'cart_data': cart_data,
            'totalCartItems': totalCartItems,
            'cart_total_amount': cart_total_amount,
            'isUserAuthenticated': request.user.is_authenticated
        }
        cartListContext = render_to_string("core/async/cart-list.html",
                                           context)  # we use this fn render_to_string, so that page refresh naa ho , appa sirf html change kr dyiye
        return Response({'data': cartListContext, 'totalCartItems': totalCartItems, 'error': error})

    def delete(self, request):
        cart_total_amount =0
        product_id = str(request.data['id'])
        if not request.user.is_authenticated:
            if 'cart_data_obj' in request.session:
                if product_id in request.session['cart_data_obj']:
                    cart_data = request.session['cart_data_obj']
                    del cart_data[product_id]
                    request.session['cart_data_obj'] = cart_data
            if 'cart_data_obj' in request.session:
                for p_id, item in request.session['cart_data_obj'].items():
                    cart_total_amount += int(item['qty']) * float(item['price'])
            totalCartItems= len(request.session['cart_data_obj'])
            cart_data = request.session['cart_data_obj']
        else:
            product = Product.objects.filter(pid=product_id).first()
            c = CartData.objects.filter(product=product, user=request.user)
            totalCartItems = c.count()
            if totalCartItems > 0:
                c.delete()
            else:
                error = 'Product not present for logged in user !'
            cart_data = CartData.objects.filter(user=request.user)
            for data in cart_data:
                amt = float(data.product.price) * (data.qty)
                cart_total_amount += amt
            totalCartItems = cart_data.count()
        context = {
            'cart_data': cart_data,
            'totalCartItems': totalCartItems,
            'cart_total_amount': cart_total_amount,
            'isUserAuthenticated': request.user.is_authenticated
        }
        print("ggn 271", context)
        try:
            cartListContext = render_to_string("core/async/cart-list.html",
                                               context)  # we use this fn render_to_string, so that page refresh naa ho , appa sirf html change kr dyiye
        except Exception as e:
            print("ggn 274", e)

        return Response({'data': cartListContext, 'totalCartItems': totalCartItems})

class WishlistView(APIView):
    http_method_names = ['get', 'post', 'delete']
    renderer_classes = (JSONRenderer,)
    def get(self, request):
        print("ggn 195", request.user)
        if not request.user.is_authenticated:
            wishlists = {}
            if 'wishlist_data_obj' in request.session:
                wishlists = request.session['wishlist_data_obj']
            isUserAuthenticated = False
        else:
            try:
                wishlists = Wishlist.objects.filter(user=request.user)
            except:
                wishlists = None
            isUserAuthenticated = True
        context = {
            "wishlists": wishlists,
            "isUserAuthenticated": isUserAuthenticated
        }
        return render(request, 'core/wishlist.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            wishlist_product = {}
            productId = str(request.data['product_id'])
            product = Product.objects.get(id=productId)
            wishlist_product[productId] = {
                'title': product.title,
                'in_stock': product.in_stock,
                'price': f"{product.price:.2f}", # float format
                'image': product.image.url
            }
            if 'wishlist_data_obj' in request.session:
                wishlist_data = request.session['wishlist_data_obj']
                wishlist_data.update(wishlist_product)
                request.session['wishlist_data_obj'] = wishlist_data
            else:
                request.session['wishlist_data_obj'] = wishlist_product
            wishlist_count =len(request.session['wishlist_data_obj'])
            context = {
                'bool': True,
                'wishlist_count': wishlist_count
            }
            return Response(context)
        else:
            product_id = request.data['product_id']
            product = Product.objects.get(id=product_id)
            wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
            if wishlist_count > 0:
                dataAdded = False
            else:
                new_wishlist = Wishlist.objects.create(
                    product=product,
                    user=request.user,
                )
                dataAdded = True
                wishlist_count = Wishlist.objects.filter(user=request.user).count()
            context = {
                'bool': dataAdded,
                'wishlist_count': wishlist_count
            }
            return Response(context)

    def delete(self, request):
        if not request.user.is_authenticated:
            wishlist_id = {}
            isUserAuthenticated = False
            product_id = str(request.data['wishlist_id'])
            if 'wishlist_data_obj' in request.session:
                if product_id in request.session['wishlist_data_obj']:
                    wishlist_data = request.session['wishlist_data_obj']
                    del wishlist_data[product_id]
                    request.session['wishlist_data_obj'] = wishlist_data
                wishlists = request.session['wishlist_data_obj']
            wishlistCount = len(wishlists)
        else:
            print("ggn 357", request.data)
            isUserAuthenticated = True
            idToBeDeleted = request.data['wishlist_id']
            print("ggn 357", idToBeDeleted)
            wishlist_d = Wishlist.objects.filter(id=idToBeDeleted)
            print("ggn 361", wishlist_d)
            delete_product = wishlist_d.delete()  # j error aya te _d.objects.delete
            wishlists = Wishlist.objects.filter(user=request.user)
            qs = serializers.serialize('json', wishlists)  # bcz jsonResponse ch querySet nhi bhej skde
            wishlistCount = wishlists.count()
        context = {
            "wishlists": wishlists,
            "isUserAuthenticated": isUserAuthenticated
        }
        print("ggn 368", context)
        # qs_json = serializers.serialize('json', wishlist)
        data = render_to_string('core/async/wishlist.html', context)
        return Response({'data': data, 'wishlist_count': wishlistCount})


def index(request, *args):
    # product = Product.objects.all().order_by("-id")
    product = Product.objects.filter(featured=True)
    deals = []
    for p in product:
        if p.get_percentage()>50:
            deals.append(p)
    statusProducts = Product.objects.filter(status=True)
    # category = Category.objects.all()
    context = {
        "products": product,
        "statusProducts": statusProducts,
        "deals": deals
    }
    return render(request, "core/index.html", context) # in html file, key of context is treated as variable

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

@login_required
def checkout(request):
    profile = Profile.objects.filter(user=request.user)
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        context = {
            'cart_data': request.session['cart_data_obj'],
            'totalCartItems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'profile': profile
        }

    else:
        context = {
            'cart_data': {},
            'totalCartItems': 0,
            'cart_total_amount': 0,
            'user': request.user
        }

    return render(request, "core/checkout.html", context)

@api_view(["GET"])
def tag_list(request, tag_slug=None): # name is what we enter, slug is entered acc to name, if space is in name, slug will replace it with hyphen(-)
    if request.method=="GET":
        products = Product.objects.filter(product_status="published").order_by("-id")


        if tag_slug:
            print("ggn 150")
            tag = Tag.objects.filter(slug=tag_slug)
            # tag = get_object_or_404(Tag, slug=tag_slug)
            print("ggn 151", tag)
            if tag:
                tag = tag[0]
                tagName = tag.name
                product = products.filter(tags__in=[tag]) # the tags in tags__in is field name in Product table
            else:
                tagName = tag_slug
                product = None
        context = {
            'products': product,
            'tag': tagName
        }
        print("ggn 155", context)
        return render(request, "core/tag.html", context)

# if not logged in , then show alert

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def product_add_review(request, pid):
    if not request.user.is_authenticated:
        return Response({
        'bool': False,
        'context': {}
        })
    else:
        product = Product.objects.get(pid=pid)
        user = request.user
        review = ProductReview.objects.create(
            user = user,
            product = product,
            review = request.POST['review'],
            rating = request.POST['rating']
        )
        context = {
            'user': user.username,
            'review': request.POST['review'],
            'rating': request.POST['rating'],

        }
        return Response({
            'bool': True,
            'context': context
        })

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def search_view(request):
    query = request.GET.get("searchForItems")
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        'products': products,
        'query': query
    }
    return render(request, "core/search.html", context)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    priceRangeFrom = request.GET['priceRangeFrom']
    priceRangeTo = request.GET['priceRangeTo']

    if priceRangeFrom!='':
        priceRangeFrom= int(priceRangeFrom)
    if priceRangeTo!='':
        priceRangeTo= int(priceRangeTo)
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    if len(categories)>0:
        products = products.filter(category__cid__in=categories).distinct()
    if len(vendors)>0:
        products = products.filter(vendor__vid__in=vendors).distinct()
    products = products.filter(price__range=(priceRangeFrom, priceRangeTo))
    context = {
        'products': products
    }
    data = render_to_string("core/async/product-list.html", context)
    return Response({
        "data": data,
        'totalProductsAfterFilter': len(products)
    })


def make_default_address(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})


