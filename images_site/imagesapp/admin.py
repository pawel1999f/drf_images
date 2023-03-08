from django.contrib import admin

# Register your models here.

from .models import AccountTier, LinkModel, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.register(AccountTier)
# admin.site.register(LinkModel)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)