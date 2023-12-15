from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Account
from .forms import ContactForm, ProfileForm, UserForm, UserUpdateForm




def user_index(request):
    try:
        user_acc =Account.objects.get(user = request.user)
        return HttpResponse(
            f"Приложение USERS, {request.user} | {request.user.id} | {user_acc.nickname}, {request.GET}")
    except:
        return HttpResponse('не авторизован')




def contact_page(request):
    """страница обратной связи"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено', form.cleaned_data)
            return redirect("users_app:contact_page")
        else:
            print('Ошибка', form.errors)

    else:
        form = ContactForm()
    us = request.user

    context = {'form': form, 'user': us}
    return render(request, 'users/contact_page.html', context)


def register_request(request):
    """страница регистрации нового пользователя"""
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Авторы')
            user.groups.add(group)
            login(request, user)
            #messages.success(request, "Registration successful." )
            return redirect("users_app:user_account")
        '''else:
            messages.error(request, "Unsuccessful registration. Invalid information.")'''
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, "users/registration.html", context)


@login_required(login_url='users_app:login')
def user_account(request):
    """страница редактирования профиля пользователя"""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, ('Your profile was successfully updated!'))
            #return redirect("users_app:contact_page")
        """else:
            messages.error(request, ('Unable to complete request'))"""

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.account)

    return render(request=request, template_name="users/user_profile.html",
                  context={"user": request.user, "user_form": user_form, "profile_form": profile_form})




def login_request(request):
    """страница входа для зарегистрированного пользователя"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.info(request, f"You are now logged in as {username}.")
                return redirect("users_app:user_account")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})






def logout_request(request):
    """страница выхода из профиля"""
    logout(request)
    #messages.info(request, "You have successfully logged out.")
    return redirect("news_app:index")



from django.urls import reverse_lazy
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """страница изменения пароля"""
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users_app:user_profile')
