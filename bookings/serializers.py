from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = '__all__'
		read_only_fields = ['id', 'user', 'status', 'created_at']

	def create(self, validated_data):
		request = self.context.get('request')
		user = request.user if request else None
		validated_data.pop('user', None)

		booking = Booking.objects.create(user=user, **validated_data)

		return booking
