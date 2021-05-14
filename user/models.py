from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from recipe.models import Recipe

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE, related_name='favorites'
    )


class OrderList(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE, related_name='order_list'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE, related_name='order_list'
    )
