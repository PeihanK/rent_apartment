from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from adverts.models import Advert
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class CreateReviewView(generics.CreateAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		advert_id = self.kwargs.get('advert_id')
		try:
			advert = Advert.objects.get(id=advert_id)
		except Advert.DoesNotExist:
			raise ValidationError('Advert not found.')
		user = self.request.user

		if not advert.bookings.filter(user=user, status='CONFIRMED').exists():
			raise ValidationError('You can leave a comment after booking confirmation only')

		serializer.save(user=user, advert=advert)


class ListReviewView(generics.ListAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [AllowAny]

	def get_queryset(self):
		advert_id = self.kwargs.get('advert_id')
		return Review.objects.filter(advert_id=advert_id)
