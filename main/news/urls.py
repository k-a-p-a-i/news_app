from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('news/', views.new_req, name='news'),
    path('user_account/', views.user_account, name='user_account'),
]
