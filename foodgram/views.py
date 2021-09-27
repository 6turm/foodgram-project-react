from django.shortcuts import render


def page_not_found(request, exception):
    return render(
        request, "error404.html",
        {
            "path": request.path,
            "title": "Ошибка 404",
        },
        status=404
    )


def server_error(request):
    return render(
        request, "error500.html",
        {
            "path": request.path,
            "title": "Ошибка 500",
        },
        status=500
    )