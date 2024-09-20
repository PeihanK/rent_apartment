import datetime
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from django.utils.timezone import make_aware


class CreateBookingView(generics.CreateAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		advert = serializer.validated_data['advert']
		start_date = serializer.validated_data['start_date']
		end_date = serializer.validated_data['end_date']

		booking = Booking(
			user=self.request.user,
			advert=advert,
			start_date=start_date,
			end_date=end_date,
		)

		if not booking.availability():
			raise ValidationError('This booking is not available for this dates')

		booking.save()
		serializer.save(user=self.request.user)


class ConfirmBookingView(generics.UpdateAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]

	def update(self, request, *args, **kwargs):
		booking = self.get_object()
		if booking.advert.owner != request.user:
			raise PermissionDenied('You do not have permission to confirm this booking')
		booking.status = 'CONFIRMED'
		booking.save()

		serializer = self.get_serializer(booking)
		return Response(serializer.data, status=status.HTTP_200_OK)


class CancelBookingView(generics.UpdateAPIView):
	queryset = Booking.objects.all()
	permission_classes = [IsAuthenticated]

	def update(self, request, *args, **kwargs):
		booking = self.get_object()

		cancel_deadline = make_aware(
			datetime.datetime.combine(booking.start_date, datetime.time.min)
		) - datetime.timedelta(days=2)

		if booking.user != request.user:
			raise PermissionDenied('You do not have permission to cancel this booking')

		if cancel_deadline < timezone.now():
			raise ValidationError('You can only cancel this booking at least 2 days before the check-in date')

		booking.status = 'CANCELLED'
		booking.save()

		return Response({'status': 'Booking cancelled'}, status=status.HTTP_200_OK)


class BookingListView(generics.ListAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user)
