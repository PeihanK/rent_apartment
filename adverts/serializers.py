from rest_framework import serializers
from adverts.models import Advert


class AdvertSerializer(serializers.ModelSerializer):
	class Meta:
		model = Advert
		fields = '__all__'
		read_only_fields = ('owner', 'created_at', 'updated_at')


class AdvertCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Advert
		fields = ['title', 'description', 'address', 'price', 'room_count', 'housing_type', 'is_active']


