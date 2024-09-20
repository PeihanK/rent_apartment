from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from adverts.views import AdvertListView, AdvertDetailView, AdvertCreateView, AdvertUpdateView, AdvertDeleteView
from bookings.views import CreateBookingView, ConfirmBookingView, CancelBookingView, BookingListView
from reviews.views import ListReviewView, CreateReviewView
from users.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterUserView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Rent Apartment API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('adverts/', AdvertListView.as_view(), name='adverts-list'),
    path('adverts/<int:pk>/', AdvertDetailView.as_view(), name='advert-detail'),
    path('adverts/create/', AdvertCreateView.as_view(), name='advert-create'),
    path('adverts/<int:pk>/update/', AdvertUpdateView.as_view(), name='advert-update'),
    path('adverts/<int:pk>/delete/', AdvertDeleteView.as_view(), name='advert-delete'),
    path('adverts/<int:advert_id>/reviews/', ListReviewView.as_view(), name='reviews-list'),
    path('adverts/<int:advert_id>/reviews/create/', CreateReviewView.as_view(), name='reviews-create'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', CreateBookingView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/confirm/', ConfirmBookingView.as_view(), name='booking-confirm'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
