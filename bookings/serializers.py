from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = '__all__'
		read_only_fields = ['id', 'user', 'status', 'created_at']

	def get_available_dates(self, obj):							# get available dates
		return Booking.get_available_dates(obj.advert)

	def validate(self, attrs):
		start_date = attrs.get('start_date')
		end_date = attrs.get('end_date')
		advert = attrs.get('advert')

		if start_date and end_date:

			conflicting_bookings = Booking.objects.filter(
				advert=advert,
				status__in=['confirmed', 'pending'],
				start_date__lt=end_date,
				end_date__gt=start_date
			)
			if conflicting_bookings.exists():
				raise serializers.ValidationError("These dates are already booked.")

		return attrs

	def create(self, validated_data):
		request = self.context.get('request')
		user = request.user if request else None
		validated_data.pop('user', None)

		booking = Booking.objects.create(user=user, **validated_data)

		return booking
