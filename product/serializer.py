from rest_framework import serializers
from .models import Product, CartItem, ProductReview, ProductRating
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


class ProductListReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductReview
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class ProductListRatingSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductRating
        fields = "__all__"


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'description', 'name', 'price', 'seller', 'category', 'reviews', 'rating']

    def get_reviews(self, obj):
        reviews = obj.productreview_set.values_list('text', flat=True)
        return list(reviews)

    def get_rating(self, obj):
        ratings = ProductRating.objects.filter(product=obj)
        total_ratings = ratings.count()
        if total_ratings == 0:
            return 0  # No ratings yet
        total_sum = sum(rating.rating for rating in ratings)
        average = total_sum / total_ratings
        return average
