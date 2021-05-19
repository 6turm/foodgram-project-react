from django.shortcuts import render
from .models import Recipe
from django.core.paginator import Paginator


def index(request):
    recipe_list = Recipe.objects.all()  # select_related('имя связи') - для кэширования связанных объектов
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        index.html,
        {'page': page, 'paginator': paginator}
    )
