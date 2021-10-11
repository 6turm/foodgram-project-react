from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Favorite, Follow, OrderList, Product

from .serializers import (FavoriteSerializer, FollowSerializer,
                          OrderListSerializer, ProductSerializer)


class AddToFavorites(APIView):

    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            response = Response(
                {'success': True}, status=status.HTTP_201_CREATED
            )
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class RemoveFromFavorites(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request, pk, format=None):
        Favorite.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class Subscribe(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            response = Response(
                {'success': True}, status=status.HTTP_201_CREATED
            )
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class UnSubscribe(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request, pk, format=None):
        Follow.objects.filter(user=request.user, author_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class GetProducts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, format=None):
        serializer = ProductSerializer(data=request.query_params)
        if serializer.is_valid():
            text = serializer.validated_data['title']
            products = list(
                Product.objects.filter(title__icontains=text).values(
                    'title', 'dimension'
                )
            )
            response = JsonResponse(products, safe=False)
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class AddPurchase(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        serializer = OrderListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            response = Response(
                {'success': True}, status=status.HTTP_201_CREATED
            )
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return response


class RemovePurchase(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request, pk, format=None):
        OrderList.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
