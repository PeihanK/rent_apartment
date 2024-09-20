from django.db import models
from users.models import User


class Advert(models.Model):
	HOUSING_TYPE_CHOICES = [
		('apartment', 'Apartment'),
		('house', 'House'),
		('castle', 'Castle'),
		('villa', 'Villa'),
		('camping', 'Camping'),
	]
	title = models.CharField(max_length=100)
	description = models.TextField()
	address = models.TextField(max_length=100)
	price = models.IntegerField()
	room_count = models.IntegerField()
	housing_type = models.CharField(max_length=40, choices=HOUSING_TYPE_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adverts')
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Advert'
		verbose_name_plural = 'Adverts'
		ordering = ['-created_at']
