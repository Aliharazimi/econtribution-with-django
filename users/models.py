from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from autoslug import AutoSlugField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	image = models.ImageField(upload_to='profile_pics', default='default.jpg')
	phone_number = PhoneNumberField(region="NG")
	bio = models.TextField(blank=True, null=True)
	amount = models.FloatField(default=0.00)

	def __str__(self):
		return f'profile of {self.user.username}'


class Contribution(models.Model):
	CATEGORY_CHOICES = [
	('MR','Wedding'),
	('BD','Birthday'),
	('EV','Event'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='MR')
	amount_needed = models.FloatField(default=0.00)
	amount_contributed = models.FloatField(default=0.00)
	description = models.TextField(blank=True, null=True)
	contributor_count = models.IntegerField(default=1)
	slug = AutoSlugField(populate_from='title', editable=True, always_update=True)
	created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return f'Event for {self.user.username}'


class Contributor(models.Model):
	CHOICES = [('PU','Public'),('OG','Organizer'), ('AN','Anonymous')]
	transaction_id = models.CharField(max_length=20, blank=True, null=True)
	contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	amount_deposited = models.FloatField(blank=True, null=True)
	short_message = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=10, blank=True, null=True)
	audiance = models.CharField(choices=CHOICES, max_length=3, default='PU')
	created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.name} contributed to {self.contribution.title}'


class ContactUs(models.Model):
	email = models.EmailField(blank=True, null=True)
	phone_number = PhoneNumberField(region="NG")
	message = models.TextField(blank=True, null=True)

class Withdrawal(models.Model):
	contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
	account_number = models.CharField(max_length=15, blank=True, null=True)
	account_name = models.CharField(max_length=100, blank=True, null=True)
	bank = models.CharField(max_length=100, blank=True, null=True)
	amount = models.FloatField(blank=True, null=True)
	status = models.CharField(max_length=20, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)