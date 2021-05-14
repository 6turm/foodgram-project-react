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
    image = models.ImageField(upload_to='/recipe', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    consist = models.ManyToManyField(
        Product, through='Ingredien', on_delete=SET_NULL, null=True,
    )
    tag = models.ManyToManyField(
        Tag, on_delete=SET_NULL, null=True, related_name='recipes'
    )
    coocking_time = models.TimeField(validators=[])
    pub_date = models.DurationField(verbose_name='Дата публикации')
    slug = models.SlugField(verbose_name='Рецепт')

    class Meta:
        ordering = ['-pub_date']


class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=PROTECT, related_name='+')
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE, related_name='ingredients'
    )
    amount = models.IntegerField()

    # def __str__(self):
    #     return f'{self.product.title}, {self} {self.product.measure}'
