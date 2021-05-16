from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email')
    empty_value_display = '-пусто-'
    list_filter = UserAdmin.list_filter + ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)