from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from captcha.models import CaptchaStore
from ..models import UserMessage
from ..forms import ContactUsForm, UserLoginForm, UserPasswordChangeForm, UserRegistrationForm


class RegistrationForm(TestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.form_data = {
            "username": "illia",
            "email": "example@gmail.com",
            "password1": "password1234!",
            "password2": "password1234!"
        }

    def test_valid_data(self):
        valid_data = self.form_data.copy()
        valid_form = UserRegistrationForm(data=valid_data)
        self.assertTrue(valid_form.is_valid())
        valid_form.save()
        self.assertTrue(get_user_model().objects.filter(username="illia").exists())

    def test_invalid_username(self):
        form_data = self.form_data.copy()
        form_data['username'] = ""
        invalid_form = UserRegistrationForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_email(self):
        form_data = self.form_data.copy()
        form_data['email'] = "not valid email"
        invalid_form = UserRegistrationForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())

    def test_email_is_taken(self):
        form_data = self.form_data.copy()
        user = UserRegistrationForm(data=form_data)
        user.save()
        invalid_form = UserRegistrationForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_password(self):
        form_data = self.form_data.copy()
        form_data['password1'] = "1234"
        form_data['password2'] = "1234"
        invalid_form = UserRegistrationForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())
        
    def test_passwords_not_match(self):
        form_data = self.form_data.copy()
        form_data['password2'] = "password123456789!"
        invalid_form = UserRegistrationForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())
        

class LoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {"username": "illia", "password": "password1234!"}
        get_user_model().objects.create_user(username=cls.form_data['username'], password=cls.form_data['password'])

    def test_valid_data(self):
        form_data = self.form_data.copy()
        valid_form = UserLoginForm(data=form_data)
        self.assertTrue(valid_form.is_valid())
        
        user = authenticate(username=form_data['username'], password=form_data['password'])
        self.assertIsNotNone(user)

    def test_invalid_username(self):
        form_data = self.form_data.copy()
        form_data['username'] = "alex"
        invalid_form = UserLoginForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_password(self):
        form_data = self.form_data.copy()
        form_data['password'] = "123456789!"
        invalid_form = UserLoginForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())
        

class PasswordChangeForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.passwords = {"old_password": "password1234!", "new_password1": "new_password", "new_password2": "new_password"}
        cls.user = get_user_model().objects.create_user(username="illia", password=cls.passwords['old_password'])

    def test_valid_data(self):
        valid_data = self.passwords.copy()
        valid_form = UserPasswordChangeForm(user=self.user, data=valid_data)
        self.assertTrue(valid_form.is_valid())

    def test_invalid_old_password(self):
        invalid_data = self.passwords.copy()
        invalid_data['old_password'] = "invalid password"
        invalid_form = UserPasswordChangeForm(user=self.user, data=invalid_data)
        self.assertFalse(invalid_form.is_valid())

    def test_new_password_not_match(self):
        invalid_data = self.passwords.copy()
        invalid_data['new_password1'] = "invalid password"
        invalid_form = UserPasswordChangeForm(user=self.user, data=invalid_data)
        self.assertFalse(invalid_form.is_valid())
        invalid_data['new_password1'], invalid_data['new_password2'] = invalid_data['new_password2'], invalid_data['new_password1']
        invalid_form = UserPasswordChangeForm(user=self.user, data=invalid_data)
        self.assertFalse(invalid_form.is_valid())


class ContactForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        cls.form = ContactUsForm(data={
            "full_name": 'illia',
            'email': "example_email@gmail.com",
            'comment': "test comment",
            'captcha_0': captcha.hashkey,
            'captcha_1': captcha.response})
    
    def test_valid_data(self):
        valid_data = self.form.data 
        valid_form = ContactUsForm(data=valid_data)
        self.assertTrue(valid_form.is_valid())
        valid_form.save()
        self.assertTrue(UserMessage.objects.filter(comment="test comment").exists())      

    def test_invalid_email(self):
        form_data = self.form.data
        form_data['email'] = "not valid email"
        invalid_form = ContactUsForm(data=form_data)

        self.assertFalse(invalid_form.is_valid())

    def test_invalid_comment(self):
        form_data = self.form.data
        form_data["comment"] = ""
        invalid_form = ContactUsForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_captcha(self):
        form_data = self.form.data
        form_data["captcha_0"] = "not valid captcha"
        invalid_form = ContactUsForm(data=form_data)
        self.assertFalse(invalid_form.is_valid())