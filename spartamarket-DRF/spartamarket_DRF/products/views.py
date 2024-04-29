from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_product(request, productId):
    try:
        product = Product.objects.get(id=productId)
    except Product.DoesNotExist:
        return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        # 수정 권한 확인
        if request.user == product.user:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        # 삭제 권한 확인
        if request.user == product.user:
            product.delete()
            return Response("Product deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)
