from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **extra_fields):
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	STATUS_CHOICES = [
		('customer', 'Customer'),
		('host', 'Host'),
	]
	username = models.CharField(max_length=120, unique=True, error_messages={
		'unique': 'A user with that username already exists.'
	})
	email = models.EmailField(max_length=100, unique=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='customer')
	created_at = models.DateTimeField(auto_now_add=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'status', ]

	objects = UserManager()

	def __str__(self):
		return self.email

	class Meta:
		db_table = 'users'
		verbose_name = 'User'
		unique_together = ['email']
		ordering = ['-created_at']
