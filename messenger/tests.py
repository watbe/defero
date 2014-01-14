from django.test import TestCase
from messenger.models import Officer, BaseMessage, Conversation
from django.contrib.auth import get_user_model
import messenger.messenger_methods as mess
import uuid

TEST_ITERATIONS = 10


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
        officer = mess.get_officer_or_false(get_user_model().objects.get(username="pleb"))

        self.assertFalse(officer)
        self.assertEqual(mess.get_officer_or_false(get_user_model().objects.get(username="tester")).user,
                         get_user_model().objects.get(username="tester"))


class MessengerTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username="tester")

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
        pass  # TODO

    def test_conversation_access_control(self):
        c1, m1 = mess.new_conversation_from_message("TEST")
        c1.save()
        m1.save()

        tester = get_user_model().objects.get(username="tester")

        # Check that tester has no access to conversation
        self.assertFalse(mess.get_conversation_or_false(c1.uuid, tester))

        print("Passed access denied test")

        c1.recipients.add(tester)
        c1.save()

        # Check that tester now can access it and it returns the right thing
        self.assertEqual(mess.get_conversation_or_false(c1.uuid, tester), c1)

        print("Passed access allowed test")

    def test_reply_access_control(self):
        """
        Test that replies don't alter access control
        """
        pass # TODO


    # TODO Test that anonymous users cannot see any conversations.

    # TODO Test that conversations are properly associated with accounts if they are signed in already.
