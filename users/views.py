import jwt
from django.http import Http404
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework import permissions, status
from .serializers import SellerSerializer, CustomerSerializer, MyTokenObtainPairSerializer, \
    SellerProfileSerializer, CustomerProfileSerializer
from .models import Seller, Customer, MyUser
from product.models import Cart
from .permissions import AnonPermission
import requests


class LoginView(TokenObtainPairView):
    permission_classes = (AnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class SellerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            # email = request.data['email']
            # url = f"https://api.emailhunter.co/v2/email-verifier?email={email}&api_key=51590a7516dd4855a2192a6ed4018e757006cc67"
            # response = requests.get(url)
            # data = response.json()
            # email_verify = data["data"]["status"]
            # if email_verify == "invalid":
            #     raise ValidationError("Email doesn't exist")
            seller = Seller.objects.create(
                email=request.data['email'],
                is_Seller=True,
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                description=request.data['description']
            )
            seller.set_password(request.data['password'])
            seller.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # email = request.data['email']
            # url = f"https://api.emailhunter.co/v2/email-verifier?email={email}&api_key=51590a7516dd4855a2192a6ed4018e757006cc67"
            # response = requests.get(url)
            # data = response.json()
            # email_verify = data["data"]["status"]
            # if email_verify == "invalid":
            #     raise ValidationError("Email doesn't exist")
            customer = Customer.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                card_number=request.data['card_number'],
                address=request.data['address'],
                post_code=request.data['post_code'],
            )
            customer.set_password(request.data['password'])
            customer.save()
            Cart.objects.create(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        seller_users = Seller.objects.all()
        serializer = SellerSerializer(seller_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        customer_users = Customer.objects.all()
        serializer = CustomerSerializer(customer_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerProfileView(RetrieveAPIView):
    queryset = Seller.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SellerProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('id')
        return get_object_or_404(Seller, id=user_id)


class CustomerProfileView(RetrieveAPIView):
    queryset = Customer.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('id')
        return get_object_or_404(Customer, id=user_id)


class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if hasattr(user, 'seller'):
            serializer = SellerProfileSerializer(user.seller)
        else:
            serializer = CustomerProfileSerializer(user.customer)
        return Response(serializer.data)


class UserProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        user = MyUser.objects.get(id=id)
        if hasattr(user, 'seller'):
            serializer = SellerProfileSerializer(user.seller)
        else:
            serializer = CustomerProfileSerializer(user.customer)
        return Response(serializer.data)