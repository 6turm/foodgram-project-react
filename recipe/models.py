from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.expressions import Exists, OuterRef

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(unique=True, max_length=50, verbose_name='Слаг')
    color = models.CharField(
        max_length=50, default='orange', verbose_name='Цвет'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.slug}'


class Product(models.Model):
    '''
    Доступные продукты (наименование, единицы измерения)
    '''
    title = models.CharField(
        max_length=225, verbose_name='Название'
    )
    dimension = models.CharField(max_length=50, verbose_name='Ед. изм.')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f'{self.title}, {self.dimension}'


class RecipeQuerySet(models.QuerySet):
    def annotate_favorites(self, user_id):
        queryset = self.annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=user_id,
                recipe_id=OuterRef('pk')
            )
        ))
        return queryset


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=225,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe/',
        verbose_name='Картинка',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    consists = models.ManyToManyField(
        Product,
        through='Ingredient',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    coocking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}, от {self.author}'


class Ingredient(models.Model):
    '''
    Ингридиенты в заказе: Продукт + количество.
    '''
    product = models.ForeignKey(
        Product,
        on_delete=PROTECT,
        verbose_name='Продукт'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    amount = models.FloatField(
        validators=[
            MinValueValidator(0, 'Количество не может быть отрицательным')
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Подписан на'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favor'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class OrderList(models.Model):
    user = models.ForeignKey(
        User, on_delete=CASCADE,
        related_name='order_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=CASCADE,
        related_name='order_list',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='uniq_order'
            )
        ]
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'
