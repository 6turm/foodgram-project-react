from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipe.models import Favorite, Follow, OrderList, Product, Recipe

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe_id')

    class Meta:
        model = Favorite
        fields = ('id',)

    def create(self, validated_data):
        favorite = Favorite.objects.get_or_create(
            user_id=validated_data['user_id'],
            recipe_id=validated_data['recipe_id']
            )
        return favorite

    def validate_id(self, id):
        if not Recipe.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                f'There is no Recipe for this id: {id}'
                )
        return id


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author_id')

    class Meta:
        model = Follow
        fields = ('id',)

    def create(self, validated_data):
        follow = Follow.objects.get_or_create(
            user_id=validated_data['user_id'],
            author_id=validated_data['author_id']
            )
        return follow

    def validate_id(self, id):
        if not User.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                f'There is no User for this id: {id}'
                )
        return id


class OrderListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe_id')

    class Meta:
        model = Follow
        fields = ('id',)

    def create(self, validated_data):
        purchase = OrderList.objects.get_or_create(
            user_id=validated_data['user_id'],
            recipe_id=validated_data['recipe_id']
            )
        return purchase

    def validate_id(self, id):
        if not Recipe.objects.filter(id=id).exists():
            raise serializers.ValidationError(
                f'There is no Recipe for this id: {id}'
                )
        return id


class ProductSerializer(serializers.ModelSerializer):
    query = serializers.CharField(source='title', allow_blank=True)

    class Meta:
        model = Product
        fields = ('query',)

    def validate_query(self, data):
        if data.__contains__('query'):
            raise serializers.ValidationError(
                f'"query" param is required, recived: {data}'
                )
        return data
