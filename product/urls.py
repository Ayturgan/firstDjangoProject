from django.urls import path
from .views import ProductCreateAPIView, ProductListAPIView, ProductDetailAPIView, ProductUpdateAPIView, \
    ProductDeleteAPIView, CartAddProductAPIView, CartListAPIView

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('list/', ProductListAPIView.as_view(), name='product-list'),
    path('list/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('update/<int:id>/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('delete/<int:id>/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('cart/<int:id>/add-product/', CartAddProductAPIView.as_view(), name='add-product-to-cart'),
    path('cart/<int:id>/', CartListAPIView.as_view(), name='cart-list'),
]
