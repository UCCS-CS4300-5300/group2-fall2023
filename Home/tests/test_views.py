'''This module holds all tests for the Home app views.'''
### CS 4300 Fall 2023 Group 2
### Harvestly
### Test Home Views (Including Signup/Login)

import re
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User



class HomeTests(TestCase):
    """ Test the Home view """

    def test_home_at_url(self):
        """ Verify that the home view exists at `/` """

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


    def test_home_at_reverse_lookup(self):
        """ Verify that the home view exists with reverse lookup of `index` """

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)


    def test_home_uses_template(self):
        """ Verify that the home view uses the correct template """

        self.client.get(reverse("index"))

        self.assertTemplateUsed("home.html")


    def test_home_uses_layout(self):
        """ Verify that the home view uses the layout template """

        self.client.get(reverse("index"))

        self.assertTemplateUsed("layout.html")


class AboutTests(TestCase):
    """ Test the About view """

    def test_about_at_url(self):
        """ Verify that the about view exists at `/about-us/` """

        response = self.client.get("/about-us/")

        self.assertEqual(response.status_code, 200)


    def test_about_at_reverse_lookup(self):
        """ Verify that the about view exists with reverse lookup of `about` """

        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)


    def test_about_uses_template(self):
        """ Verify that the about view uses the correct template """

        self.client.get(reverse("about"))

        self.assertTemplateUsed("about.html")


    def test_about_uses_layout(self):
        """ Verify that the about view uses the layout template """

        self.client.get(reverse("about"))

        self.assertTemplateUsed("layout.html")


class SignUpTests(TestCase):
    """ Test the SignUp view """

    def test_sign_up_at_url(self):
        """ Verify that the sign up view exists at `/signup/` """

        response = self.client.get("/signup/")

        self.assertEqual(response.status_code, 200)


    def test_sign_up_at_reverse_lookup(self):
        """ Verify that the sign up view exists with reverse lookup of `signup` """

        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)


    def test_sign_up_uses_template(self):
        """ Verify that the signup view uses the correct template """

        self.client.get(reverse("signup"))

        self.assertTemplateUsed("registration/signup.html")


    def test_sign_up_uses_layout(self):
        """ Verify that the signup view uses the layout template """

        self.client.get(reverse("signup"))

        self.assertTemplateUsed("layout.html")

    def test_sign_up_valid_form(self):
        """ Test a valid sign up form submission """

        new_username = "username1"
        data = {
            "username": new_username,
            "password1": "test_password_12345",
            "password2": "test_password_12345",
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=new_username).exists())


    def test_sign_up_missing_username(self):
        """ Test a sign up form submission without a username """

        data = {
            "password1": "test_password_12345",
            "password2": "test_password_12345",
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")


    def test_sign_up_missing_password1(self):
        """ Test a sign up form submission without a password """

        data = {
            "username": "username1",
            "password2": "test_password_12345",
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_sign_up_missing_password2(self):
        """ Test a sign up form submission without a password confirmation """

        data = {
            "username": "username1",
            "password1": "test_password_12345",
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")


    def test_sign_up_mismatched_passwords(self):
        """ Test a sign up form submission with mismatched passwords """

        data = {
            "username": "username1",
            "password1": "test_password_12345",
            "password2": "test_password_789",
        }

        response = self.client.post(reverse("signup"), data)

        self.assertEqual(response.status_code, 200)

        pattern = re.escape("The two password fields didn") + r"[\u2019 ']" + re.escape("t match.")
        self.assertTrue(pattern, response.content.decode("utf-8"))


class LoginTests(TestCase):
    """ Test the Login view """

    def setUp(self):
        """ Set up a user to validate against """

        self.username = "username1"
        self.password = "test_password_12345"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()


    def test_login_at_url(self):
        """ Verify that the login view exists at `/accounts/login/` """

        response = self.client.get("/accounts/login/")

        self.assertEqual(response.status_code, 200)


    def test_login_at_reverse_lookup(self):
        """ Verify that the login view exists with reverse lookup of `login` """

        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)


    def test_login_uses_template(self):
        """ Verify that the login view uses the correct template """

        self.client.get(reverse("login"))

        self.assertTemplateUsed("registration/login.html")


    def test_login_uses_layout(self):
        """ Verify that the login view uses the layout template """

        self.client.get(reverse("login"))

        self.assertTemplateUsed("layout.html")


    def test_login_valid_form(self):
        """ Test a valid login form submission """

        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(reverse("login"), data)

        self.assertEqual(response.status_code, 302)


    def test_login_missing_username(self):
        """ Test a login form submission where the username is missing """

        data = {
            "password": self.password,
        }

        response = self.client.post(reverse("login"), data)

        self.assertEqual(response.status_code, 200)

        # Unsure about this since Django already helps valiate here
        # self.assertContains(response, "This field is required.") TODO


    def test_login_missing_password(self):
        """ Test a login form submission where the password is missing """

        data = {
            "username": self.username,
        }

        response = self.client.post(reverse("login"), data)

        self.assertEqual(response.status_code, 200)

        # Unsure about this since Django already helps valiate here
        # self.assertContains(response, "This field is required.") TODO


    def test_login_user_does_not_exist(self):
        """ Test a login form submission where the user does not exist """

        data = {
            "username": "invalid_username",
            "password": "invalid_password"
        }

        response = self.client.post(reverse("login"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
        self.assertContains(response, "Note that both fields may be case-sensitive.")
        