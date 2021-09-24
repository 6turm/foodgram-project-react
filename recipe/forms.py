from django import forms
from django.contrib.auth import get_user_model
from .models import Recipe, Product
from django.utils.translation import ugettext_lazy
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    initial_text = 'Текущее изображение'

    input_text = 'Изменить'

    clear_checkbox_label = 'Удалить'


forms.Field.default_error_messages = {
    'required': ugettext_lazy("Это поле обязательно для заполнения."),
}


User = get_user_model()

class RecipeForm(forms.ModelForm):
    ingredients = forms.IntegerField(required=False)  # Поле для реализации вывода ошибок
    def __init__(self, *args, **kwargs):
        self.ingredients = kwargs.pop('ingredients', None)
        super(RecipeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'description', 'coocking_time', 'image')
        widgets = {'tag': forms.CheckboxSelectMultiple(), 'image': CustomClearableFileInput() }
    
    def clean(self):
        cleaned_data = super(RecipeForm, self).clean()
        if len(self.ingredients) < 1:
            self.add_error('ingredients', 'Необходимо добавить ингридиенты!')
        else:
            for name in self.ingredients.keys():
                if name not in Product.objects.all().values_list('title', flat=True):
                    self.add_error('ingredients', f'Данного продукта нет в базе: {name}.')
        return cleaned_data
