from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('user', 'advert', 'advert_id', 'start_date', 'end_date', 'status')
	search_fields = ('user', 'advert_title')
	list_filter = ('status', 'start_date', 'end_date', 'created_at')
	list_editable = ('status', 'start_date', 'end_date')
	ordering = ('status', '-created_at')

