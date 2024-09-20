from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny

from adverts.models import Advert
from adverts.serializers import AdvertSerializer, AdvertCreateUpdateSerializer


class AdvertListView(generics.ListAPIView):
	serializer_class = AdvertSerializer
	permission_classes = [AllowAny]

	def get_queryset(self):
		queryset = Advert.objects.filter(is_active=True)
		params = self.request.query_params

		# filter by owner
		owner = params.get('owner')
		if owner:
			queryset = queryset.filter(owner_id=owner)

		# search by keyword
		search_query = params.get('search')
		if search_query:
			queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

		# filter by price
		min_price = params.get('min_price')
		max_price = params.get('max_price')
		if min_price:
			queryset = queryset.filter(price__gte=min_price)
		if max_price:
			queryset = queryset.filter(price__lte=max_price)

		# filter by address
		address = params.get('address')
		if address:
			queryset = queryset.filter(address__icontains=address)

		# filter by rooms
		min_rooms = params.get('min_rooms')
		max_rooms = params.get('max_rooms')
		if min_rooms:
			queryset = queryset.filter(room_number__gte=min_rooms)
		if max_rooms:
			queryset = queryset.filter(room_number__lte=max_rooms)

		# filter by housing type
		housing_type = params.get('housing_type')
		if housing_type:
			queryset = queryset.filter(housing_type__icontains=housing_type)

		# sort by price
		sort_by_price = params.get('sort_by_price')
		if sort_by_price == 'min_to_max':
			queryset = queryset.order_by('price')
		elif sort_by_price == 'max_to_min':
			queryset = queryset.order_by('-price')

		# sort by created date
		sort_by_date = params.get('sort_by_date')
		if sort_by_date == 'newest':
			queryset = queryset.order_by('-created_at')
		elif sort_by_date == 'oldest':
			queryset = queryset.order_by('created_at')

		return queryset


class AdvertDetailView(generics.RetrieveAPIView):
	queryset = Advert.objects.all()
	serializer_class = AdvertSerializer
	permission_classes = [AllowAny]


class AdvertCreateView(generics.CreateAPIView):
	serializer_class = AdvertCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		if self.request.user.status != 'host':
			raise PermissionDenied("Only hosts can create adverts.")
		serializer.save(owner=self.request.user)


class AdvertUpdateView(generics.RetrieveUpdateAPIView):
	queryset = Advert.objects.all()
	serializer_class = AdvertCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		advert = super().get_object()
		if advert.owner != self.request.user:
			raise PermissionDenied("You don't have permission to edit this advert.")
		if self.request.user.status != 'host':
			raise PermissionDenied("Only hosts can edit adverts.")
		return advert


class AdvertDeleteView(generics.DestroyAPIView):
	queryset = Advert.objects.all()
	permission_classes = [IsAuthenticated]

	def get_object(self):
		advert = super().get_object()
		if advert.owner != self.request.user:
			raise PermissionDenied("You don't have permission to delete this advert.")
		if self.request.user.status != 'host':
			raise PermissionDenied("Only hosts can create adverts.")
		return advert
