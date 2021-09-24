from django import template

register = template.Library()


@register.filter(name='update_tag_url')
def update_tag_url(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist('tag'):
        tags = new_request.getlist('tag')
        tags.remove(tag.slug)
        new_request.setlist('page', [])
        new_request.setlist('tag', tags)
    else:
        new_request.setlist('page', [])
        new_request.appendlist('tag', tag.slug)
    return new_request.urlencode()


@register.filter(name='update_paginator_url')
def update_paginator_url(request, page_num):
    new_request = request.GET.copy()
    new_request.setlist('page', [page_num])
    return new_request.urlencode()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
