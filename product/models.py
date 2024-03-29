from django.db.models import *
from users.models import Seller, Customer


class Category(Model):
    name = CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255, null=False)
    description = TextField()
    price = IntegerField(null=False)
    seller = ForeignKey(Seller, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Cart(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, related_name='cart')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name


class CartItem(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE, related_name='items')
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)


class ProductRating(Model):
    user = ForeignKey(Customer, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    rating = PositiveIntegerField()

    def __str__(self):
        return f'Rating by {self.user.email} for {self.product.name}'


class ProductReview(Model):
    author = ForeignKey(Customer, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    text = TextField()
    create_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.author.email} for {self.product.name}'
