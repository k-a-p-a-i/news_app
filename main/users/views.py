from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.core.paginator import Paginator


from .models import Account, FavoriteArticle
from .forms import ContactForm, ProfileForm, UserForm, UserUpdateForm
from .utils import check_group



def user_index(request):
    try:
        user_acc =Account.objects.get(user = request.user)
        return HttpResponse(
            f"Приложение USERS, {request.user} | {request.user.id} | {user_acc.nickname}, {request.GET}")
    except:
        return HttpResponse('не авторизован')



##-----------------------Страница обратной связи(только для авторизованных)_________________________#######################
@check_group()
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST, initial={'email': request.user.email, 'name':request.user.username})
        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, ('Сообщение отправлено'))
            return redirect("users_app:contact_page")
        else:
            print('Ошибка', form.errors)

    else:
        form = ContactForm(initial={'email': request.user.email, 'name':request.user.username})
    us = request.user

    context = {'form': form, 'user': us}
    return render(request, 'users/contact_page.html', context)



##-----------------------Регистрация нового пользователя_________________________#######################
def register_request(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            category = request.POST['account_type']

            if category == 'author':
                group = Group.objects.get(name='Необходимо утверждение')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Читатель')
                user.groups.add(group)

            login(request, user)
            return redirect("users_app:user_account")
        else:
            messages.error(request, "Не удалось зарегистрировать пользователя")
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, "users/registration.html", context)





##-----------------------Обновление профиля_________________________#######################
@login_required(login_url='users_app:login', )
def user_account(request):

    if request.method == "POST" and 'changing_profile' in request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Данные профиля обновлены'))
            return HttpResponseRedirect(request.path_info)

        """else:
            messages.error(request, ('Unable to complete request'))"""

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.account)


    return render(request=request, template_name="users/user_profile.html",
                  context={"user": request.user, "user_form": user_form, "profile_form": profile_form})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Ваш пароль успешно изменен')
            return redirect('users_app:user_account')
        else:
            messages.error(request, 'Неправильно введены данные')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {
        'password_form': form})







##-----------------------Авторизация_________________________#######################
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли в аккаунт {username}")
                return redirect("users_app:user_account")
            else:
                messages.error(request, "Неправильное имя пользователя или пароль")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})


##-----------------------Выход из профиля_________________________#######################
def logout_request(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect("news_app:index")


##-----------------------Удаление аккаунта_________________________#######################
@login_required
def profile_delete(request):
    user = request.user
    user.delete()
    messages.info(request, "Аккаунт удален")
    return redirect("news_app:index")




from news.models import Article

##-----------------------Добавить в избранное_________________________#######################
@login_required
def add_to_favorites(request, id):
    article = Article.objects.get(id=id)
    bookmark = FavoriteArticle.objects.filter(user = request.user.id, article = article)

    if bookmark.exists():
        bookmark.delete()
        messages.warning(request, 'Закладка удалена')

    else:
        bookmark = FavoriteArticle.objects.create(user = request.user, article=article)
        messages.success(request, 'Добавлено в избранное')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

    total = len(articles)
    p = Paginator(articles,2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {'articles': page_obj, 'total':total, 'bookmark':bookmark }
    #           'categories':categories,'selected_category': selected_category}

    return render(request,'users/my_news_list.html',context)





from news.utils import ArticleTable
from news.filters import ArticleFilter
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

##-----------------------Избранные новости_________________________#######################
class FavoriteArticleListView(SingleTableMixin,FilterView):
    model = Article
    table_class = ArticleTable
    filterset_class = ArticleFilter
    paginate_by = 15
    template_name = 'users/my_favorite.html'

    def get_queryset(self):
        bookmark_id = FavoriteArticle.objects.filter(user=self.request.user.id).values_list('article_id', flat=True)
        favorite_article = Article.objects.filter(id__in=bookmark_id)
        return favorite_article

