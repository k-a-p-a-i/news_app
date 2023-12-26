from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin


from .models import Account, FavoriteArticle




class UserProfileInline(admin.StackedInline):
    model = Account
    max_num = 1
    can_delete = False



def make_author(modeladmin, request, queryset):
    group = Group.objects.get(name = 'Авторы')
    ungroup = Group.objects.get(name = 'Необходимо утверждение')
    for user in queryset:
        user.groups.add(group)
        user.groups.remove(ungroup)

make_author.short_description = "Утвердить автора"

class UserAdmin(UserAdmin):
    #inlines = [UserProfileInline]
    actions = [make_author]
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)


@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'create_at']


# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)





