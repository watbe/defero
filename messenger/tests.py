from django.test import TestCase
from messenger.models import Officer, BaseMessage, AnonymousMessage, Reply, Conversation
from django.contrib.auth import get_user_model
import messenger.messenger_methods as mess
import uuid

TEST_ITERATIONS = 2000


class OfficerTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="tester")
        officer = Officer.objects.create(user=user, role="Test Officer")
        not_officer = get_user_model().objects.create(username="pleb")
        officer.save()
        not_officer.save()

    def test_officer_string(self):
        """
        Test that the output of the officer's role matches the role name, to ensure that we don't give away
        the username of the officer user.
        """
        user = get_user_model().objects.get(username="tester")
        officer = Officer.objects.get(user=user)
        self.assertEqual(officer.__str__(), officer.role)

    def test_get_officer(self):
        """
        Tests the get_officer function
        """
        officer = mess.get_officer(get_user_model().objects.get(username="pleb"))

        self.assertFalse(officer)
        self.assertEqual(mess.get_officer(get_user_model().objects.get(username="tester")).user,
                         get_user_model().objects.get(username="tester"))


class MessengerTestCase(TestCase):

    def test_unique_conversations(self):
        """
        Test that the method creates unique UUIDs for each conversation
        """
        for x in range(TEST_ITERATIONS):
            mess.new_conversation()

        print('Created %d new conversations' % (x+1))

        # Ensure that any uuid is discovered only once
        x = 0
        for conversation in Conversation.objects.all():
            x += 1
            try:
                Conversation.objects.get(uuid=conversation.uuid)
            except Conversation.MultipleObjectsReturned:
                self.fail()

        print('Checked %d conversations' % x)

    def test_uuid_regex(self):
        """
        Check that our UUID regex matches correctly
        """
        for x in range(TEST_ITERATIONS):
            self.assertTrue(mess.uuid_check(uuid.uuid4().__str__()))

        print('Checked regex against %d UUIDs' % (x+1))

    def test_new_message_uniqueness(self):
        """
        Test that views.new_message creates unique conversations by setting up a fake AnonymousMessage and checking
        that the response object contains a unique URL.
        """
        pass