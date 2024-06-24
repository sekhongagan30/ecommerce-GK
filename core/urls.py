from django.urls import path
from core import views # we can simply write it as from views import index; but for better understanding, wrote core.views

app_name = "core" # what is its use?

urlpatterns = [
    path('', views.index , name="indexOfHomePage"), # name is used in redirect, we simple pass this name in core: redirect("core:index")
    path('about/', views.about , name="about"), # name is used in redirect, we simple pass this name in core: redirect("core:index")
    path('contact/', views.contact , name="contact"), # name is used in redirect, we simple pass this name in core: redirect("core:index")
    path('checkout/', views.checkout , name="checkout"), # name is used in redirect, we simple pass this name in core: redirect("core:index")

    path('products/', views.ProductView.as_view() , name="product-list"),
    path('product/<pid>/', views.ProductView.as_view() , name="product-detail"),

    # category
    path('category/', views.CategoryView.as_view() , name="category-list"),
    path('category/<cid>/', views.CategoryView.as_view(), name="category-product-list"),

    # vendor
    path('vendors/', views.VendorView.as_view(), name="vendor-list"),
    path('vendor/<vid>/', views.VendorView.as_view(), name="vendor-detail"),

    # Tags
    path('products/tag/<slug:tag_slug>', views.tag_list, name="tags"),

    # Add review
    path('add-review/<str:pid>/', views.product_add_review, name="add-review"),

    # Search
    path('search/', views.search_view, name="search"),

    # Filtering products
    path('filter-products/', views.filter_product, name="filter-products"),

    # Adding to cart
    path('add-to-cart/', views.CartView.as_view(), name="add-to-cart"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('delete-from-cart/', views.CartView.as_view(), name="delete-from-cart"),
    path('update-cart/', views.CartView.as_view(), name="update-cart"),

    # wishlist
    path('wishlist/', views.WishlistView.as_view(), name="wishlist"),
    path('add-to-wishlist/', views.WishlistView.as_view(), name="add-to-wishlist"),
    path('remove-from-wishlist/', views.WishlistView.as_view(), name="remove-from-wishlist"),
    path('make-default-address/', views.make_default_address, name="make-default-address"),

]