from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Product(models.Model):
    title = models.CharField(unique=True, max_length=225, db_index=True)
    measure = models.CharField(max_length=50)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE, related_name='author')
    title = models.CharField(max_length=225, verbose_name='Название')
    image = models.ImageField(upload_to='/recipe')
    description = models.TextField(verbose_name='Описание')
    consist = models.ManyToManyField(Product, through='Ingredien')
    tag = models.ManyToManyField(Tag, on_delete=SET_NULL, related_name='+')

    class Meta:
        ordering = []


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=PROTECT, related_name='+')
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE, related_name='ingredients'
    )
    amount = models.IntegerField()

    def __str__(self):
        pass
