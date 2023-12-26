from django.urls import path
from . import views

app_name = "news_app"


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news/', views.ArticleListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.ArticleDetailView.as_view(), name='single_news'),
    path('update/<int:pk>/', views.ArticleUpdatelView.as_view(), name='update_news'), #корректировка новости
    path('news/add', views.add_news, name='add_news'),                             #добавление новости
    path('delete/<int:pk>/', views.ArticleDeletelView.as_view(), name='delete_news'),      #удаление новости
    path('search_news/', views.search_news, name='search_news'),      #поиск новостей
    path('autosuggest/', views.autosuggest, name='autosuggest'),      #автоподставление
    path("my_news_list/", views.AuthorListView.as_view(), name= "my_news_list"), #список новостей автора
    path("add_tag_category/", views.add_tag_category, name= "add_tag_category"), #список новостей автора


]
