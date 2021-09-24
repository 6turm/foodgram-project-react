from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from recipe.models import Favorites, Follow, Ingredient, Product


class AddToFavorites(APIView):
    def post(self, request, format=None):
        print('@@@@ ', request.data)
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
    def get(self, request):
        text = request.GET['query']
        products = list(
            Product.objects.filter(title__icontains=text).values('title', 'dimension')
            )
        return JsonResponse(products, safe=False)
