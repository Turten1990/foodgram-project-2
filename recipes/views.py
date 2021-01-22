import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


from .forms import RecipeForm
from .models import (
    Follow,
    Favorite,
    Recipe,
    Tag,
    User,
    ShopList
)


class RecipeListView(ListView):
    """Выводит список всех рецептов на главную страницу"""

    template_name = "index.html"
    model = Recipe
    context_object_name = "recipe_list"
    paginate_by = 6

    def __init__(self, **kwargs) -> None:
        self.all_tags = Tag.objects.all()
        super().__init__(**kwargs)

    def get_queryset(self):  # -> QuerySet:
        queryset = super().get_queryset()

        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset


class AuthorListView(RecipeListView):
    """Выводит список всех рецептов одного автора"""

    def get_queryset(self):
        self.author = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        self.queryset = self.model._default_manager.filter(author=self.author)
        return super().get_queryset()


class FollowList(LoginRequiredMixin, ListView):
    """Добавляет/удаляет автора в подписки + отображение."""

    template_name = "follow.html"
    paginate_by = 3

    def get_queryset(self):  # -> QuerySet:
        queryset = User.objects.filter(following__user=self.request.user)
        return queryset

    def post(self, request):
        """ Обрабатывает POST-запрос от JS при нажатии на кнопку "Подписаться" """
        req_ = json.loads(request.body)
        author_id = req_.get("id", None)
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            obj, created = Follow.objects.get_or_create(
                user=request.user, author=author
            )

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        """ Обрабатывает POST-запрос от JS при нажатии на кнопку "Отписаться" """
        author = get_object_or_404(Follow, user=request.user, author=author_id)
        author.delete()
        return JsonResponse({"success": True})


class Favorites(LoginRequiredMixin, RecipeListView):
    """Добавляет/удаляет рецепта в "Избранное" + отображение."""

    def get_queryset(self):
        self.queryset = self.model._default_manager.filter(
            favorites__user=self.request.user
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = True
        return context

    def post(self, request):
        """ Обрабатывает POST-запрос от JS при нажатии на "звездочку" """
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        """ Обрабатывает POST-запрос от JS при отжатии "звездочки" """
        recipe = get_object_or_404(
            Favorite, user=request.user, recipe=recipe_id
        )
        recipe.delete()
        return JsonResponse({"success": True})


class ShopListView(ListView):
    """Добавляет/удаляет рецепты в список покупок + отображение."""

    template_name = "shop_list.html"
    model = Recipe
    context_object_name = "recipe_list"

    def get_queryset(self):  # -> QuerySet:
        queryset = Recipe.objects.filter(purchases__user=self.request.user)
        return queryset

    def post(self, request):
        """ Обрабатывает POST-запрос от JS. Добавляет рецепт в список покупок """
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = ShopList.objects.get_or_create(
                user=request.user, recipe=recipe
            )

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        """ Обрабатывает POST-запрос от JS. Удаляет рецепт из спика покупок """
        recipe = get_object_or_404(
            ShopList, user=request.user, recipe=recipe_id
        )
        recipe.delete()
        return JsonResponse({"success": True})


@login_required
def subscriptions(request):
    """ Выводит список записей авторов, которые есть в подписке """
    recipe_list = Recipe.objects.filter(
        author__following__user=request.user
    ).order_by("-pub_date")
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "myFollow.html", {"page": page, "paginator": paginator}
    )


def purchases(request):
    return render(request, "shopList.html")


class RecipeCreate(LoginRequiredMixin, CreateView):
    # model = Recipe
    form_class = RecipeForm
    template_name = "recipe_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeView(DetailView):
    model = (
        Recipe  # https://docs.djangoproject.com/en/3.1/ref/class-based-views/
    )
    template_name = "recipe_detail.html"


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    form_class = RecipeForm
    model = Recipe
    template_name = "recipe_form.html"
    # fields = ["title", "image", "text", "ingredients", "tag", "duration"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe-list")
