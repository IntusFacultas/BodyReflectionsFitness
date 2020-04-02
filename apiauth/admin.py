from django.contrib import admin
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.


class ProfileModelAdmin(admin.ModelAdmin):
    model = Profile


class ProfileAdmin(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileAdmin]


admin.site.register(Profile, ProfileModelAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
