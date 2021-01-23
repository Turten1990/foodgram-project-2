from django import template
from django.http import request

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter
def get_filter_values(get_params):
    return get_params.getlist("tags")


@register.filter
def get_filter_link(get_params, tag):
    # get_params = get_params.copy()
    tags: list = get_params.getlist("tags")
    if tag.slug in tags:
        tags.remove(tag.slug)
        # get_params.setlist("tags", tags)
    else:
        tags.append(tag.slug)
        # get_params.update({"tags": tag.slug})

    if tags:
        result = "tags=" + "&tags=".join(tags)
        return result

    # return get_params.urlencode()

@register.filter
def get_tags(get_params):
    tags = get_params.getlist("tags")
    if tags:
        result = "tags=" + "&tags=".join(tags)
        # result = "tags="
        # for tag in tags:
        #     result += "&tags=".join(tags)
        return result