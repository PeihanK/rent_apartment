from django.db import models
from adverts.models import Advert
from users.models import User
from datetime import timedelta, date


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
		unique_together = ('advert', 'user', 'start_date', 'end_date')
		verbose_name = 'Booking'
		verbose_name_plural = 'Bookings'
		ordering = ['-created_at']

	def availability(self):							# available dates
		booked_dates = Booking.objects.filter(
			advert=self.advert,
			status='confirmed',
			start_date__lt=self.end_date,
			end_date__gt=self.start_date
		)
		return not booked_dates.exists()

	@staticmethod									# booked dates
	def get_booked_dates(advert):
		booked_dates = Booking.objects.filter(
			advert=advert,
			status='confirmed'
		).values('start_date', 'end_date')

		dates = []
		for booking in booked_dates:
			current_date = booking['start_date']
			while current_date <= booking['end_date']:
				dates.append(current_date)
				current_date += timedelta(days=1)

		return dates

	@staticmethod									# available dates 1 year ahead
	def get_available_dates(advert):
		today = date.today()
		one_year_ahead = today + timedelta(days=365)
		booked_dates = Booking.get_booked_dates(advert)

		available_dates = []
		current_date = today
		while current_date <= one_year_ahead:
			if current_date not in booked_dates:
				available_dates.append(current_date)
			current_date += timedelta(days=1)

		return available_dates


