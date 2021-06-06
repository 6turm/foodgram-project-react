from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from recipe.models import Favorites, Follow


class AddToFavorites(APIView):
    def post(self, request, format=None):
        # print(request.data['id'], type(request.data['id']))
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
