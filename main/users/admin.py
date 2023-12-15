from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


from .models import Account




class UserProfileInline(admin.StackedInline):
    model = Account
    max_num = 1
    can_delete = False

class UserAdmin(UserAdmin):
    #inlines = [UserProfileInline]
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)



# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)





