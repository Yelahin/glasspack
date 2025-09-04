from django.test import TestCase
from captcha.models import CaptchaStore
from ..models import UserMessage
from ..forms import ContactUsForm


class ContactForm(TestCase):
    #utils
    def get_captcha_example(self):
        captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
        return captcha

    #tests
    def test_valid_data(self):
        captcha =captcha = self.get_captcha_example()
        form = ContactUsForm(data={
                             "full_name": 'illia',
                             'email': "example_email@gmail.com",
                             'comment': "test comment",
                             'captcha_0': captcha.hashkey,
                             'captcha_1': captcha.response})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['comment'], 'test comment')

    def test_not_valid_email(self):
        captcha =captcha = self.get_captcha_example()
        form = ContactUsForm(data={
                             "full_name": 'illia',
                             'email': "not-an-email",
                             'comment': "test comment",
                             'captcha_0': captcha.hashkey,
                             'captcha_1': captcha.response})
        self.assertIn('email', form.errors)

    def test_not_valid_comment(self):
        captcha =captcha = self.get_captcha_example()
        form = ContactUsForm(data={
                             "full_name": 'illia',
                             'email': "example_email@gmail.com",
                             'comment': " ",
                             'captcha_0': captcha.hashkey,
                             'captcha_1': captcha.response})
        self.assertIn('comment', form.errors)

    def test_not_valid_captcha(self):
        captcha =captcha = self.get_captcha_example()
        form = ContactUsForm(data={
                             "full_name": 'illia',
                             'email': "example_email@gmail.com",
                             'comment': "test comment",
                             'captcha_0': captcha.hashkey,
                             'captcha_1': 'nothing'})
        self.assertIn('captcha', form.errors)

    def test_save_data(self):
        captcha = self.get_captcha_example()
        form = ContactUsForm(data={
                             "full_name": 'illia',
                             'email': "example_email@gmail.com",
                             'comment': "test comment",
                             'captcha_0': captcha.hashkey,
                             'captcha_1': captcha.response})
        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertIsInstance(obj, UserMessage)
        self.assertEqual(UserMessage.objects.count(), 1)
        self.assertEqual(UserMessage.objects.first(), obj)
        self.assertEqual(UserMessage.objects.first().full_name, 'illia')
        self.assertEqual(UserMessage.objects.first().email, 'example_email@gmail.com')
        self.assertEqual(UserMessage.objects.first().comment, 'test comment')
        