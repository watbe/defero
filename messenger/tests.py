from django.test import TestCase
from messenger.models import Officer, BaseMessage, AnonymousMessage, Reply, Conversation
from django.contrib.auth import get_user_model


class OfficerTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="tester")
        Officer.objects.create(user=user, role="Test Officer")

    def test_officer_string(self):
        user = get_user_model().objects.get(username="tester")
        officer = Officer.objects.get(user=user)
        self.assertEqual(officer.__str__(), officer.role)
