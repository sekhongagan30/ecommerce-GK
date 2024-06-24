from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager # installed pip install django-taggit
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = [
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
]

STATUS = [
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
]

RATING = [
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
]

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcd123")
    title= models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta: # this name is shown as the table name in admin panel
        verbose_name_plural = "Categories" # to avoid admin to write Categorys

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# class Tags(models.Model):
#     pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcd123")
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the best vendor")
    description = models.TextField(null=True, blank=True, default="This is the best vendor")
    address = models.CharField(max_length=100, default="Model Town, Jalandhar")
    contact = models.CharField(max_length=100, default="+91 123456789")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted, do u wanna del the shop?
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # if user is deleted, then null=True allows this field to be null, if nullFalse, then django will show related error
    # with foreign key, u can directly use all cols of that table like user.UserTableCol1
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Vendors" # to avoid admin to write Categorys

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcd123")

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # if user is deleted, then null=True allows this field to be null, if nullFalse, then django will show related error
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="categoryRelatedToProduct")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name="vendorRelatedToProduct")

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = models.TextField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=999999999, decimal_places = 2, default="2.99")

    # specifications = models.TextField(null=True, blank=True)
    specifications = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, default="Organic", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    life = models.CharField(max_length=100, default="100 days", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products" # to avoid admin to write Categorys

    def product_image(self):
        print("ggn 104", self.image.url)
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price - self.price)/self.old_price) * 100
        return new_price

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-image", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"  # to avoid admin to write Categorys

######################################Cart, Order, OrderItem and address

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=999999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))

######################Product Reviews, wishlist, address
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # if user is deleted, then null=True allows this field to be null, if nullFalse, then django will show related error
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviewsRelatedToProduct")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Reviews" # to avoid admin to write Categorys

    def __str__(self):
        return self.product.title if self.product is not None else "Product Not exist"

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    # it is vvvimp to add prefix in ShortUUIDField
    # wid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="wish", alphabet="abcd123")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)  # if user is deleted, then null=True allows this field to be null, if nullFalse, then django will show related error
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"  # to avoid admin to write Categorys

    def __str__(self):
        return self.product.title if self.product is not None else "Product Not exist"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Address"