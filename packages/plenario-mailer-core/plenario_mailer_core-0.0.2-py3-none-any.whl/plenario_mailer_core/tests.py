from django.contrib.auth import get_user_model
from django.test import TestCase

from plenario_mailer_core import mailer

from tests.app.models import EtlEventMeta


User = get_user_model()


class TestMailer(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='test@example.com', password='shh secret')

        self.meta_model = EtlEventMeta.objects.create(
            name='test',
            contributor=self.user,
            source_url='https://example.com/')

    def tearDown(self):
        self.meta_model.delete()
        self.user.delete()

    def test_send_data_set_approved_email(self):
        mailer.send_data_set_approved_email(self.meta_model)

    def test_send_data_set_ready_email(self):
        mailer.send_data_set_ready_email(self.meta_model)

    def test_send_data_set_erred_email(self):
        mailer.send_data_set_erred_email(self.meta_model, 'test')

    def test_send_data_set_fixed_email(self):
        mailer.send_data_set_fixed_email(self.meta_model, 'test')
