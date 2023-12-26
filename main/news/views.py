from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages


from .forms import ArticleForm, ImagesFormSet, TagForm, CategoryForm
from .models import Article, ShowImage, Tag, Category
from .filters import ArticleFilter
from users.utils import check_group
from .utils import ViewCountMixin


from users.models import FavoriteArticle


def index(request):
    articles = Article.objects.all().order_by("-date")
    p = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    bookmarks = FavoriteArticle.objects.filter(user=request.user.id).values_list('article_id', flat=True)


    context = {'posts': page_obj, 'articles':  articles, 'bookmarks': bookmarks}
    return render(request, 'news/index.html', context)



def about(request):
    return render(request, 'news/about.html' )


def error_404(request, exception):
    "функция вызова ошибки 404"
    context = {}
    return render(request, 'news/404.html', context)


##-----------------------Добавление новости_________________________#######################
@check_group('Авторы')
@login_required(login_url='users_app:login')
def add_news(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id:
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save()
                form.save_m2m() #чтобы сохранилась связь многие-ко-многим
                for img in request.FILES.getlist('image_field'):
                    ShowImage.objects.create(article=new_article, image= img, title=img.name)
                return redirect(new_article)
    else:
        form = ArticleForm()
    return render(request, 'news/add_news.html', {"form": form})

##-----------------------Просмотр одной новости_________________________#######################
class ArticleDetailView(ViewCountMixin,DetailView):
    model = Article
    template_name = 'news/single_news.html'
    context_object_name = 'article'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = ShowImage.objects.filter(article = current_object)
        bookmark = FavoriteArticle.objects.filter(user=self.request.user.id, article_id=current_object.id)
        context['images'] = images
        context['bookmark'] = bookmark
        return context




##-----------------------Обновление новости_________________________#######################
class ArticleUpdatelView(UpdateView):
    model = Article
    template_name = 'news/add_news.html'
    fields = ['title', 'anouncement', 'text', 'category',  'tags']
    #success_url = reverse_lazy('news_app:news_list')

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.user.id != self.object.author.id and (not self.request.user.is_staff):
            messages.error(request, "Ошибка доступа")
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)








class ArticleDeletelView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_app:news_list')
    template_name = 'news/delete_news.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.user.id != self.object.author.id and (not self.request.user.is_staff):
            messages.error(request, "Ошибка доступа")
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)




from .utils import ArticleTable
from django_tables2 import SingleTableView, SingleTableMixin


##-----------------------Фильтрация новостей_________________________#######################
class ArticleListView(SingleTableMixin,FilterView):
    model = Article
    table_class = ArticleTable
    filterset_class = ArticleFilter
    paginate_by = 15
    template_name = 'news/news.html'



def search_news(request):
    """страница поиска новости по заголовку и аннотации"""
    search_post = request.GET.get("search")
    if search_post:
        posts = Article.objects.filter(
            Q(title__icontains=search_post) | Q(anouncement__icontains=search_post))  # | Q(text__icontains=search_post)
    else:
        posts = Article.objects.all().order_by("-date")

    context = {'posts': posts}
    return render(request, 'news/search.html', context)



##-----------------------Jquery Автозаполнение _________________________#######################
def autosuggest(request):
    query_original = request.GET.get('term')
    qs = Article.objects.filter(title__icontains=query_original)
    results = []
    results += [article.title for article in qs]
    return JsonResponse(results, safe=False)

##-----------------------Search Component in Navbar _________________________#######################
def search_news(request):
    search_post = request.GET.get("search", None)
    if search_post:
        search_query = search_post.lower().split()
        lookups = Q()
        for word in search_query:
            lookups |= Q(title__icontains=word)
        posts = Article.objects.filter(lookups)
    else:
        posts = Article.objects.all().order_by("-date")

    context = {'posts': posts}

    return render(request,'news/search.html', context)



##-----------------------Список новостей автора_________________________#######################
class AuthorListView(SingleTableMixin,FilterView):

    def get_queryset(self):
        qs = Article.objects.filter(author=self.request.user)
        return qs


    model = Article
    table_class = ArticleTable
    filterset_class = ArticleFilter
    paginate_by = 15
    template_name = 'news/my_news_list.html'


##-----------------------Добавление Тэгов и Категорий_________________________#######################
@check_group('Авторы')
@login_required(login_url='users_app:login')
def add_tag_category(request):
    tag = Tag.objects.all()
    category = Category.objects.all()
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        category_form = CategoryForm(request.POST)
        if tag_form.is_valid():
            new_tag = tag_form.save(commit=False)
            new_tag.save()
            tag_form.save_m2m() #чтобы сохранилась связь многие-ко-многим
            messages.success(request, f"Новый тэг {new_tag.title} успешно создан")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        if category_form.is_valid():
            new_category = category_form.save()
            messages.success(request, f"Новая категория {new_category.name} успешно создана")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    else:
        tag_form = TagForm()
        category_form = CategoryForm()
    return render(request, 'news/add_category.html', {"tag_form": tag_form, "category_form": category_form,
                                                      "tags": tag, "category": category})

