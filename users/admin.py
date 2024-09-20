from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'status')
	search_fields = ('username', 'email')
	list_filter = ('status', 'created_at')

