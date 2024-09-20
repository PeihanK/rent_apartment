from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import User
import re


class RegisterUserSerializer(serializers.ModelSerializer):
	re_password = serializers.CharField(max_length=128, write_only=True)

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'status',
			'password',
			're_password'
		)
		extra_kwargs = {'password': {'write_only': True}}

	def validate(self, data):
		username = data.get('username')

		if not re.match(r'^[a-zA-Z0-9_]*$', username):
			raise serializers.ValidationError('The username must be alphanumeric characters or have only _ symbol')

		password = data.get('password')
		re_password = data.get('re_password')
		if password != re_password:
			raise serializers.ValidationError("The passwords don't match")

		try:
			validate_password(password)
		except ValidationError as err:
			raise serializers.ValidationError(err.messages)

		return data

	def create(self, validated_data):
		validated_data.pop('re_password')  # Удаление re_password
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=128, write_only=True)

	def validate(self, data):
		email = data.get('email')
		password = data.get('password')

		user = authenticate(email=email, password=password)

		if not user:
			raise serializers.ValidationError("Invalid credentials")

		if not user.is_active:
			raise serializers.ValidationError("User account is disabled")

		return data
