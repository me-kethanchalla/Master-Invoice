from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login2')
        self.home_url = reverse('home')
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='StrongPass123'
        )

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertIn('login_form', response.context)

    def test_login_successful(self):
        data = {
            'login': '1',
            'username': 'testuser',
            'password': 'StrongPass123',
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.home_url)

    def test_login_nonexistent_user(self):
        data = {
            'login': '1',
            'username': 'doesnotexist',
            'password': 'whatever',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Login failed" in str(m) for m in messages))

    def test_login_wrong_password(self):
        data = {
            'login': '1',
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Login failed" in str(m) for m in messages))

    def test_login_empty_fields(self):
        data = {
            'login': '1',
            'username': '',
            'password': '',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Login failed" in str(m) for m in messages))

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTests(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpassword123'
        )
        self.url = reverse('login2')

    def test_successful_registration(self):
        response = self.client.post(self.url, {
            'register': '1',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securePassword123!',
            'password2': 'securePassword123!',
        })
        self.assertRedirects(response, reverse('verify_otp'))
        #check that user is not created yet
        self.assertFalse(User.objects.filter(username='newuser').exists())
        #check that the session contains the registration data
        self.assertIn('register_data', self.client.session)
        self.assertEqual(self.client.session['register_data']['username'], 'newuser')

    def test_registration_with_existing_username(self):
        response = self.client.post(self.url, {
            'register': '1',
            'username': 'existinguser',
            'email': 'uniqueemail@example.com',
            'password1': 'securePassword123!',
            'password2': 'securePassword123!',
        })
        self.assertContains(response, 'This username is already taken.')

    def test_registration_with_existing_email(self):
        response = self.client.post(self.url, {
            'register': '1',
            'username': 'anotheruser',
            'email': 'existing@example.com',
            'password1': 'securePassword123!',
            'password2': 'securePassword123!',
        })
        self.assertContains(response, "This email is already registered.")
