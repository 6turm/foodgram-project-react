from django.http.response import JsonResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Favorites, Follow, OrderList, Product, Recipe
from .serializers import FavoritesSerializer, FollowSerializer, OrderListSerializer


class AddToFavorites(APIView):

    def post(self, request, format=None):
        serializer = FavoritesSerializer(data=request.data)
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
    def delete(self, request, pk, format=None):
        Favorites.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class Subscribe(APIView):
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
    def delete(self, request, pk, format=None):
        Follow.objects.filter(user=request.user, author_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class GetProducts(APIView):
    def get(self, request, format=None):
        text = request.GET['query']
        print('@@@@@@ query', text)
        products = list(
            Product.objects.filter(title__icontains=text).values(
                'title', 'dimension'
                )
            )
        return JsonResponse(products, safe=False)


class AddPurchase(APIView):
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
    def delete(self, request, pk, format=None):
        OrderList.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
