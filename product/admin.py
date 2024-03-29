from django.contrib import admin
from .models import Product, Cart, CartItem, Category, ProductReview, ProductRating


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('customer', 'created_at')


admin.site.register(Cart, CartAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductReview)
admin.site.register(ProductRating)
