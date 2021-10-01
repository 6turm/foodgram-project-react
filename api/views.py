from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import Favorite, Follow, OrderList, Product

from .serializers import (FavoriteSerializer, FollowSerializer,
                          OrderListSerializer)


class AddToFavorites(APIView):

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
    def delete(self, request, pk, format=None):
        Favorite.objects.filter(user=request.user, recipe_id=pk).delete()
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
        # Не понятно, как и зачем тут проверять данные.
        # Должны возвращяться все соответсвия или ничего, если соответсвий нет.
        # Если введено любое неверное значение, как раз ничего
        # и не возвращяется. Финальная проверка введенных данных
        # выполняется в форме.
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
