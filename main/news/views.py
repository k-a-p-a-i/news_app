from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.db.models import Q

from .forms import ArticleForm
from .models import Article, ShowImage
from .filters import ArticleFilter



def index(request):
    posts = Article.objects.all().order_by("-date")
    context = {'posts': posts}
    return render(request, 'news/index.html', context)



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





def about(request):
    return render(request, 'news/about.html' )


def error_404(request, exception):
    "функция вызова ошибки 404"
    context = {}
    return render(request, 'news/404.html', context)


def news_list(request):
    "функция не используется"
    author_list = User.objects.all().values('id', 'username')
    selected = 0
    if request.method == 'POST':
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected)
    else:
        articles = Article.objects.all()
    context = {'articles': articles, 'author_list': author_list, 'selected': selected}
    return render(request, 'news/news.html', context)




@login_required(login_url='users_app:login')
def add_news(request):
    """Функция добавления новости"""
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


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/single_news.html'
    context_object_name = 'article'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = ShowImage.objects.filter(article = current_object)
        context['images'] = images
        return context

class ArticleUpdatelView(UpdateView):
    model = Article
    template_name = 'news/add_news.html'
    fields = ['title', 'anouncement', 'text', 'category',   'tags']
    success_url = reverse_lazy('news_app:news_list')




class ArticleDeletelView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_app:news_list')  #после удаление переносит на эту страницу
    template_name = 'news/delete_news.html'


class ArticleListView(FilterView):
    model = Article
    template_name = 'news/news.html'
    paginate_by = 10
    filterset_class = ArticleFilter
