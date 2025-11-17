from django.contrib.auth import get_user_model
from django.test import TestCase
from captcha.models import CaptchaStore
from django.urls import reverse
from glasspack_users.forms import ContactUsForm, UserLoginForm, UserRegistrationForm
from glasspack_users.models import UserMessage

class RegistrationPages(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = UserRegistrationForm(data={
            "username": "illia", 
            "email": "example@gmail.com", 
            "password1": "password1234!",
            "password2": "password1234!"
        })

    #Register page
    def test_register_page_use_correct_template(self):
        response = self.client.get(reverse('glasspack_users:sign_up'))
        self.assertTemplateUsed(response, 'glasspack_users/registration.html')

    def test_register_page_complete_valid_form(self):
        form_data = self.form.data
        self.assertTrue(UserRegistrationForm(data=form_data).is_valid())
        response = self.client.post(path=reverse('glasspack_users:sign_up'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('glasspack_users:register_done'))
        self.assertTrue(get_user_model().objects.filter(username="illia").exists())

    def test_register_page_complete_invalid_form(self):
        form_invalid_data = self.form.data
        form_invalid_data['password2'] = "some_password"
        self.assertFalse(UserRegistrationForm(data=form_invalid_data).is_valid())
        response = self.client.post(path=reverse('glasspack_users:sign_up'), data=form_invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="illia").exists())

    #Register done page

    def test_register_done_page_user_correct_template(self):
        response = self.client.get(reverse('glasspack_users:register_done'))
        self.assertTemplateUsed(response, "glasspack_users/register_done.html")


class LoginPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(username="illia", password="password1234!")

    def test_login_page_use_correct_template(self):
        response = self.client.get(reverse('glasspack_users:login'))
        self.assertTemplateUsed(response, 'glasspack_users/login.html')

    def test_login_page_redirect_to_home_page(self):
        user_data = {"username": "illia",  "password": "password1234!"}
        self.assertTrue(UserLoginForm(data=user_data).is_valid())
        response = self.client.post(path=reverse('glasspack_users:login'), data=user_data)
        self.assertRedirects(response, expected_url=reverse("home"))

    def test_login_page_invalid_form(self):
        user_data = {"username": "illia",  "password": "different password!"}
        self.assertFalse(UserLoginForm(data=user_data).is_valid())
        response = self.client.post(path=reverse('glasspack_users:login'), data=user_data)
        self.assertEqual(response.status_code, 200)


class ProfilePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username": "illia",  "password": "password1234!"}
        get_user_model().objects.create_user(username=cls.user_data['username'], password=cls.user_data['password'])

    def test_profile_page_use_correct_template(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse("glasspack_users:profile"))
        self.assertTemplateUsed(response, "glasspack_users/profile.html")

    def test_profile_page_redirects_for_anonymous_users(self):
        response = self.client.get(reverse('glasspack_users:profile'))
        self.assertRedirects(response, expected_url=reverse('glasspack_users:login') + "?next=/profile/")

    def test_profile_page_access_for_registered_users(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse('glasspack_users:profile'))
        self.assertEqual(response.status_code, 200)


class PasswordRecoveryPage(TestCase):
    def password_recovery_page_use_correct_template(self):
        response = self.client.get(reverse('glasspack_users:password_reset'))
        self.assertTemplateUsed(response, 'glasspack_users/reset_form.html')

    def password_recovery_done_page_use_correct_template(self):
        response = self.client.get(reverse('glasspack_users:password_reset_done'))
        self.assertTemplateUsed(response, 'glasspack_users/password_reset_done.html')

    def password_recovery_page_redirect_to_correct_page(self):
        email_for_recovery = {"email": "example@gmail.com"}
        response = self.client.post(path=reverse('glasspack_users:password_reset'), data=email_for_recovery)
        self.assertRedirects(response, expected_url=reverse('glasspack_users:password_reset_done'))

    def password_recovery_page_invalid_form(self):
        email_for_recovery = {"email": "invalid"}
        response = self.client.post(path=reverse('glasspack_users:password_reset'), data=email_for_recovery)
        self.assertEqual(response.status_code, 200)


class PasswordChangePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username": "illia", "password": "password1234!"}
        get_user_model().objects.create_user(username=cls.user_data['username'], password=cls.user_data['password'])

    def test_password_change_page_use_correct_template(self):
        self.client.login(username=self.user_data["username"], password=self.user_data["password"])
        response = self.client.get(reverse('glasspack_users:password_change'))
        self.assertTemplateUsed(response, 'glasspack_users/password_change.html')

    def test_password_change_done_page_use_correct_template(self):
        self.client.login(username=self.user_data["username"], password=self.user_data["password"])
        response = self.client.get(reverse('glasspack_users:password_change_done'))
        self.assertTemplateUsed(response, 'glasspack_users/password_change_done.html')

    def test_password_change_page_redirects_for_annonymous_users(self):
        response = self.client.get(reverse('glasspack_users:password_change'))
        self.assertRedirects(response, expected_url=reverse('glasspack_users:login') + "?next=/password_change/")

    def test_password_change_page_access_for_registered_users(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse('glasspack_users:password_change'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_page_redirects_to_correct_page_after_valid_form(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        form_data = {"old_password": self.user_data['password'], "new_password1": "password1234!", "new_password2": "password1234!"}
        response = self.client.post(path=reverse('glasspack_users:password_change'), data=form_data)
        self.assertRedirects(response, expected_url=reverse('glasspack_users:password_change_done'))

    def test_password_change_page_invalid_form(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        form_data = {"old_password": self.user_data['password'], "new_password1": "password", "new_password2": "password"}
        response = self.client.post(path=reverse('glasspack_users:password_change'), data=form_data)
        self.assertEqual(response.status_code, 200)


class ContactUsPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username": "illia", "password": "password1234!"}
        get_user_model().objects.create_user(username="illia", password=cls.user_data['password'])
        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        cls.form = ContactUsForm(data={
            "full_name": 'illia',
            'email': "example_email@gmail.com",
            'comment': "test comment",
            'captcha_0': captcha.hashkey,
            'captcha_1': captcha.response})
        
    def test_contact_page_redirects_for_anonymous_users(self):
        response = self.client.get(reverse('contact'))
        self.assertRedirects(response, expected_url=reverse('glasspack_users:login') + "?next=/contact/")

    def test_conteact_page_access_for_registered_users(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_use_correct_template(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'glasspack_site/contact.html')

    def test_contact_page_complete_valid_form(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        form_data = self.form.data
        response = self.client.post(path=reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserMessage.objects.filter(comment="test comment").exists())

    def test_contact_page_complete_invalid_form(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        form_data = self.form.data
        form_data["comment"] = ""
        response = self.client.post(path=reverse('contact'), data= form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserMessage.objects.filter(comment="").exists())