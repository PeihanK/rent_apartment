from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from adverts.models import Advert
from adverts.serializers import AdvertSerializer, AdvertCreateUpdateSerializer
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from bookings.models import Booking


class AdvertFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_rooms = filters.NumberFilter(field_name='room_count', lookup_expr='gte')
    max_rooms = filters.NumberFilter(field_name='room_count', lookup_expr='lte')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    search = filters.CharFilter(method='filter_by_search', label='Search by title or description')

    class Meta:
        model = Advert
        fields = ['owner', 'address', 'housing_type', 'min_price', 'max_price', 'min_rooms', 'max_rooms']

    def filter_by_search(self, queryset, name, value):
        if value:
            return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
        return queryset


class AdvertListView(generics.ListAPIView):
    queryset = Advert.objects.filter(is_active=True)
    serializer_class = AdvertSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertFilter
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
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
            raise PermissionDenied("Only hosts can delete adverts.")
        return advert


class AvailableDatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, advert_id):
        try:
            advert = Advert.objects.get(id=advert_id)
        except Advert.DoesNotExist:
            raise NotFound("Advert not found")

        available_dates = Booking.get_available_dates(advert)
        return Response({'available_dates': available_dates})


class MyAdvertsListView(generics.ListAPIView):
    serializer_class = AdvertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.status == 'host':
            # current host's adverts only
            return Advert.objects.filter(owner=user).distinct()
        else:
            return Advert.objects.none()