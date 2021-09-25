from django.http.response import JsonResponse
from recipe.models import Favorites, Follow, OrderList, Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AddToFavorites(APIView):
    def post(self, request, format=None):
        Favorites.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    def delete(self, request, pk, format=None):
        Favorites.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class Subscribe(APIView):
    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class UnSubscribe(APIView):
    def delete(self, request, pk, format=None):
        Follow.objects.filter(user=request.user, author_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class GetProducts(APIView):
    def get(self, request, format=None):
        text = request.GET['query']
        products = list(
            Product.objects.filter(title__icontains=text).values(
                'title', 'dimension'
                )
            )
        return JsonResponse(products, safe=False)


class AddPurchase(APIView):
    def post(self, request, format=None):
        OrderList.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
            )
        return JsonResponse({'success': True}, status=status.HTTP_200_OK)


class RemovePurchase(APIView):
    def delete(self, request, pk, format=None):
        OrderList.objects.filter(user=request.user, recipe_id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class DounloadPurchase(APIView):
    def get(self, request, format=None):
        pass
