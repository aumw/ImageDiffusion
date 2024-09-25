from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import home, profile, login_user, logout_user, register_user
from .models import Prompt, Profile
import json

# Create your tests here.

class TestUrls(TestCase):

	def test_login_url(self):
		url = reverse('login')
		self.assertEquals(resolve(url).func, login_user)

	def test_home_url(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func, home)

	# def test_profile_url(self):
	# 	url = reverse('profile')
	# 	self.assertEquals(resolve(url).func, profile)

	def test_logout_url(self):
		url = reverse('logout')
		self.assertEquals(resolve(url).func, logout_user)

	def test_register_url(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, register_user)


class TestViews(TestCase):

	def test_views_home_GET(self):
		client = Client()
		response = client.get(reverse('home'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_views_login_GET(self):
		client = Client()
		response = client.get(reverse('login'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'login.html')

	def test_views_logout_REDIRECT(self):
		client = Client()
		response = client.get(reverse('logout'))

		self.assertEquals(response.status_code, 302)
		

	def test_views_register_GET(self):
		client = Client()
		response = client.get(reverse('register'))

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'register.html')































