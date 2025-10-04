from django.test import TestCase
from django.contrib.auth import get_user_model
from home.models import UserManager, User
from django.urls import reverse

class UserModelTest(TestCase):
    def setUp(self):
        self.url_register = reverse('register')
        self.url_login = reverse('login')
        self.test_user = User.objects.create_user(
            email="tt@example.com",
            password="testpass123"
        )

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="securepass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepass123"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="nopass")

    def test_user_signup_via_url(self):
        response = self.client.post(self.url_register, {
            'email': 'test@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertRedirects(response, reverse("library"))
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_invalid_data_returns_200(self):
        url = self.url_register
        data = {
            "email": "newuser@example.com",
            "password1": "pass123",
            "password2": "wrongpass"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) # Form errors return 200
        self.assertContains(response, "The two ")    

    def test_user_login_via_url(self):
        response = self.client.post(self.url_login, {
            'username': 'tt@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse("library"))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.url_login, {
            'username': 'tt@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct")  # Default AuthenticationForm message
        self.assertNotIn('_auth_user_id', self.client.session)    

    def test_logout(self):
        self.client.login(username="tt@example.com", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("library"))
        self.assertNotIn('_auth_user_id', self.client.session)    