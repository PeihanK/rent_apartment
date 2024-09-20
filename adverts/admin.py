from django.contrib import admin
from .models import Advert


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'price', 'housing_type', 'is_active')
	search_fields = ('title', 'owner')
	list_filter = ('housing_type', 'is_active')
	ordering = ('-created_at',)

