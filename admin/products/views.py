from importlib.resources import Resource
from urllib import response
from urllib.parse import uses_fragment

from django.shortcuts import render
from .serializers import ProductSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from producer import publish

# Create your views here.
class ProductViewSet(viewsets.ViewSet):
    def list(self, request):                 # GET /api/products 
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        
    def create(self, request):  #POST /api/products
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):    # GET /api/products/<str:id>
        products = Product.objects.get(id=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    
    def update(self, request, pk=None):      # PUT /api/products/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    def destroy(self, request, pk=None):    # DELETE /api/products/<str:id>
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class UserAPIView(viewsets.ViewSet):
    def get(self, request):                 # GET /api/user
        users = User.objects.all()
        user = users[0]
        return Response ({
                'id' : user.id
            })
    def create(self, request):               # POST /api/user
        user = User.objects.create()
        return Response ({
                'type' : 'created',
                'id' : user.id
            })
        