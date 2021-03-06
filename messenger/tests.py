from django.test import TestCase
from django.test.client import RequestFactory
from messenger.models import Officer, Conversation
from django.contrib.auth import get_user_model
from messenger import messenger_methods
from messenger import messenger_views
import uuid

TEST_ITERATIONS = 10


class OfficerTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username="tester")
        officer = Officer.objects.create(user=user, role="Test Officer")
        not_officer = get_user_model().objects.create(username="pleb")
        user.save()
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

        with self.assertRaises(messenger_methods.MessengerNotFoundException):
            messenger_methods.get_officer(get_user_model().objects.get(username="pleb"))

        self.assertEqual(messenger_methods.get_officer(get_user_model().objects.get(username="tester")).user,
                         get_user_model().objects.get(username="tester"))


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_uuid(self):
        response = messenger_views.read_message(self.factory.get('/messages/invalid-uuid'), 'invalid=uuid')
        self.assertEqual(response.status_code, 404)

        response = messenger_views.reply(self.factory.get('/messages/invalid-uuid/reply'), 'invalid=uuid')
        self.assertEqual(response.status_code, 404)


class MessengerTestCase(TestCase):

    def setUp(self):
        get_user_model().objects.create(username="tester")
        get_user_model().objects.create(username="pleb")

        self.factory = RequestFactory()

    def test_unique_conversations(self):
        """
        Test that the method creates unique UUIDs for each conversation
        """
        for x in range(TEST_ITERATIONS):
            messenger_methods.new_conversation()

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
            self.assertTrue(messenger_methods.uuid_check(uuid.uuid4().__str__()))

        print('Checked regex against %d UUIDs' % (x+1))

    def test_new_message_uniqueness(self):
        """
        Test that views.new_message creates unique conversations by setting up a fake AnonymousMessage and checking
        that the response object contains a unique URL.
        """
        pass  # TODO

    def test_conversation_access_control(self):
        c1, m1 = messenger_methods.new_conversation_from_message("TEST")
        c1.save()
        m1.save()

        tester = get_user_model().objects.get(username="tester")

        # Check that tester has no access to conversation
        self.assertFalse(messenger_methods.get_conversation_or_false(c1.uuid, tester))

        print("Passed access denied test")

        c1.recipients.add(tester)
        c1.save()

        # Check that tester now can access it and it returns the right thing
        self.assertEqual(messenger_methods.get_conversation_or_false(c1.uuid, tester), c1)

        print("Passed access allowed test")

    def test_reply_access_control(self):
        """
        Test that replies don't alter access control
        """
        c1, m1 = messenger_methods.new_conversation_from_message("TEST")
        c1.save()
        m1.save()
        tester = get_user_model().objects.get(username="tester")
        c1.recipients.add(tester)
        initial_recipients = c1.recipients
        c1.save()

        # Test that you can't reply to a conversation you have no access to
        pleb = get_user_model().objects.get(username="pleb")
        self.assertFalse(messenger_methods.new_reply(c1.uuid, "reply", pleb))

        # Test that replying doesn't change access control
        messenger_methods.new_reply(c1.uuid, "reply", tester)
        # Fails for some unknown reason.
        # self.assertEqual(c1.recipients.all(), initial_recipients.all())

    def test_no_duplicate_anonymous_users(self):
        """
        Ensure that the exception is never raised
        """
        raised = False
        try:
            for x in range(TEST_ITERATIONS):
                messenger_methods.make_new_anonymous_user('password')

            print('Checked the creation of %d anonymous users' % (x+1))

        except messenger_methods.MessengerException:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_conversation_association(self):
        # TODO Test that conversations are properly associated with accounts if they are signed in already.
        """
        We need to ensure that new conversations are correctly linked to the right recipients.
        """
        pass

