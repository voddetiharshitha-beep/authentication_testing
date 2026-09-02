from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import timedelta

User = get_user_model()


class RegistrationTest(APITestCase):

    def test_registration(self):
        data = {
            "username": "newuser",
            "password": "NewPassword123"
        }

        response = self.client.post(
            "/api/auth/register/",
          data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )


class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "TestPassword123"
        }

        response = self.client.post(
          "/api/auth/login/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        data= {
            "username":"testuser",
            "password":"wrongpassword"
        }
        response=self.client.post(
            "api/auth/login/",
            data,
            format="json"
        )
        self.assertAlmostEqual(response.status_code,401)

class LogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )       
        self.refresh = RefreshToken.for_user(self.user)
  

    def test_logout(self):
        data = {
            "refresh": str(self.refresh)
        }

        response = self.client.post(
            "/api/auth/logout/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)


class PasswordChangeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_password_change(self):
        class PasswordChangeTest(APITestCase):

         def setUp(self):
          self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

        self.client.force_authenticate(user=self.user)

    def test_password_change(self):
        data = {
            "old_password": "TestPassword123",
            "new_password": "NewPassword123"
        }

        response = self.client.post(
            "/api/auth/change-password/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password("NewPassword123")
        )


class TokenRefreshTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_token_refresh(self):
        class TokenRefreshTest(APITestCase):

         def setUp(self):
           self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)

        data = {
            "refresh": str(refresh)
        }

        response = self.client.post(
            "/api/auth/token/refresh/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("access", response.data)


class ExpiredTokenTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

    def test_expired_token(self):
        # Create an access token for the user
        token = AccessToken.for_user(self.user)

        # Make the token expired
        token.set_exp(
            lifetime=timedelta(seconds=-1)
        )

        # Send the expired token in Authorization header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        # Call an endpoint that requires authentication
        response = self.client.post(
            "/api/auth/change-password/",
            {
                "old_password": "TestPassword123",
                "new_password": "NewPassword123"
            },
            format="json"
        )

        # Expired token should be rejected
        self.assertEqual(response.status_code, 401)