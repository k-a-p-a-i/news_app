from django.shortcuts import HttpResponseRedirect
from django.contrib import messages


##-----------------------Проверка на авторизацию_________________________#######################
def check_group(*groups):
     def decorator(function):
         def wrapper(request, *args, **kwargs):
             user = request.user
             if user.groups.filter(name__in=groups) or user.is_staff:
                 return function(request, *args, **kwargs)
             messages.warning(request, "Нет доступа")
             return HttpResponseRedirect(request.POST.get('next', '/')) #пересылаем пользователя туда, откуда он пришёл
         return wrapper
     return decorator