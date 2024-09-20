from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('user', 'advert', 'review', 'rating', 'created_at')
	list_filter = ('user', 'created_at')
	search_fields = ('user', 'advert')
	ordering = ('-created_at',)
