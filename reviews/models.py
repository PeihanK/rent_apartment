from django.db import models
from adverts.models import Advert
from users.models import User


class Review(models.Model):
	RATING_CHOICES = [
		(1, 1),
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5)
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='reviews')
	review = models.TextField(max_length=700)
	rating = models.IntegerField(default=0, choices=RATING_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.review

