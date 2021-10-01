from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
from django.utils.translation import ugettext_lazy

from .models import Product, Recipe


class CustomClearableFileInput(ClearableFileInput):
    initial_text = 'Текущее изображение'
    input_text = 'Изменить'
    clear_checkbox_label = 'Удалить'


forms.Field.default_error_messages = {
    'required': ugettext_lazy("Это поле обязательно для заполнения."),
}


User = get_user_model()


class RecipeForm(forms.ModelForm):
    # Поле для реализации вывода ошибок ингридиентов
    ingredients = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.ingredients = kwargs.pop('ingredients', None)
        super(RecipeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'description', 'coocking_time', 'image')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
            'image': CustomClearableFileInput(),
            'description': forms.Textarea(attrs={'rows': 8}),
            }

    def clean(self):
        cleaned_data = super(RecipeForm, self).clean()
        if len(self.ingredients) < 1:
            self.add_error('ingredients', 'Необходимо добавить ингридиенты!')
        else:
            for name in self.ingredients.keys():
                if name not in Product.objects.all().values_list(
                        'title', flat=True
                        ):
                    self.add_error(
                        'ingredients', f'Данного продукта нет в базе: {name}.'
                        )
        return cleaned_data
