from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer, CartItemSerializer
from .models import Product, Cart, CartItem
from users.permissions import IsSellerPermission, IsOwnerOrReadOnly, IsOwnerOfCart


def get_object(id, table):
    try:
        return table.objects.get(id=id)
    except table.DoesNotExist:
        raise Http404


class ProductCreateAPIView(APIView):
    permission_classes = [IsSellerPermission]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                name=request.data['name'],
                description=request.data['description'],
                price=request.data['price'],
                seller_id=request.data['seller']
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id):
        product = get_object(id, Product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsSellerPermission, IsOwnerOrReadOnly]

    def delete(self, request, id):
        product = get_object(id, Product)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class CartListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        cart = Cart.objects.get(customer=id)
        cart_items = cart.items.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAddProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, id):
        cart = Cart.objects.get(customer=id)
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        serializer = CartItemSerializer(cart_item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


