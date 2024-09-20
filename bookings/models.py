from django.db import models

from adverts.models import Advert
from users.models import User


class Booking(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('confirmed', 'Confirmed'),
		('cancelled', 'Cancelled'),
		('done', 'Done'),
	]

	advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='bookings')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
	start_date = models.DateField()
	end_date = models.DateField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} books {self.advert.title} from {self.start_date} to {self.end_date}'

	class Meta:
		verbose_name = 'Booking'
		verbose_name_plural = 'Bookings'
		ordering = ['-created_at']

	def availability(self):
		booked_dates = Booking.objects.filter(
			advert=self.advert,
			status='confirmed',
			start_date__lt=self.end_date,
			end_date__gt=self.start_date
		)
		return not booked_dates.exists()



