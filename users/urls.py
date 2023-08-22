from django.urls import path
from .views import CustomerRegisterView, SellerRegisterView, LoginView


urlpatterns = [
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='login'),
]
