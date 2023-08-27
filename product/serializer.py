from rest_framework import serializers
from .models import Product, CartItem
from users.serializers import CustomerSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customer = CustomerSerializer(source='cart.customer')

    class Meta:
        model = CartItem
        fields = "__all__"

