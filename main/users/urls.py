from django.urls import path
from . import views

app_name= 'users_app'

urlpatterns = [
    path('', views.user_index, name='user_index'),
    path('contact_page/', views.contact_page, name='contact_page'), #страница обратной связи (зедсь отдельную ссылку)
    path('registration', views.register_request, name="register"), #страница регистрации
    path('user_account/', views.user_account, name='user_account'), #профиль аккаунта
    path("login/", views.login_request, name="login"),  #страница входа в аккаунт
    path("logout/", views.logout_request, name= "logout"), #страница выхода из аккаунта
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
]
