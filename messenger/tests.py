from django.test import TestCase
from messenger.models import Officer, BaseMessage, AnonymousMessage, Reply, Conversation
from django.contrib.auth import get_user_model
import messenger.messenger_methods as mess


class OfficerTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="tester")
        Officer.objects.create(user=user, role="Test Officer")

    def test_officer_string(self):
        user = get_user_model().objects.get(username="tester")
        officer = Officer.objects.get(user=user)
        self.assertEqual(officer.__str__(), officer.role)

    def test_unique_conversations(self):
        """
        Test that the function creates unique UUIDs for each conversation
        """
        for x in range(2000):
            mess.new_conversation()

        # Ensure that any uuid is discovered only once
        for conversation in Conversation.objects.all():
            try:
                Conversation.objects.get(uuid=conversation.uuid)
            except Conversation.MultipleObjectsReturned:
                self.fail()
