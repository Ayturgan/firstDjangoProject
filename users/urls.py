from django.urls import path
from .views import CustomerRegisterView, SellerRegisterView, LoginView, SellerListAPIView, CustomerListAPIView, \
    CurrentUserProfileView, UserProfileView

urlpatterns = [
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/customers', CustomerListAPIView.as_view(), name='seller-list'),
    path('list/sellers', SellerListAPIView.as_view(), name='customer-list'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='profile'),
    path('current-profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
]
