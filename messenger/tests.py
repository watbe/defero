from django.test import TestCase
from messenger.models import Officer, BaseMessage, AnonymousMessage, Reply, Conversation
from django.contrib.auth import get_user_model
import messenger.messenger_methods as mess


class OfficerTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="tester")
        Officer.objects.create(user=user, role="Test Officer")

    def test_officer_string(self):
        """
        Test that the output of the officer's role matches the role name, to ensure that we don't give away
        the username of the officer user.
        """
        user = get_user_model().objects.get(username="tester")
        officer = Officer.objects.get(user=user)
        self.assertEqual(officer.__str__(), officer.role)

    def test_unique_conversations(self):
        """
        Test that the method creates unique UUIDs for each conversation
        """

        x = 0
        for x in range(2000):
            mess.new_conversation()

        print('Created %d new conversations' % x + 1)

        # Ensure that any uuid is discovered only once
        x = 0
        for conversation in Conversation.objects.all():
            x += 1
            try:
                Conversation.objects.get(uuid=conversation.uuid)
            except Conversation.MultipleObjectsReturned:
                self.fail()

        print('Checked %d conversations' % x)