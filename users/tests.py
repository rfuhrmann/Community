from django.test import TestCase
from users.models import User, Address, Friendship, Status, Status_Comment
import datetime


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='adam',
                                 email='adam@web.de',
                                 password='adamweb',
                                 phone='+491112223344',
                                 first_name='adam',
                                 last_name='one',
                                 )

    def test_user_is_setup(self):
        adam = User.objects.get(username="adam")
        self.assertEqual(adam.username, "adam", "Testing user model")
        self.assertEqual(adam.email, "adam@web.de")
        self.assertEqual(adam.phone, "+491112223344")
        self.assertEqual(adam.first_name, "adam")
        self.assertEqual(adam.last_name, "one")


class AddressTestCase(TestCase):
    def setUp(self):
        Address.objects.create(country="Finland",
                               postal_code=12345,
                               town="Tampere",
                               street="Main Street",
                               street_number=1,
                               )

    def test_address_is_setup(self):
        address = Address.objects.get(postal_code=12345, street_number=1)
        self.assertEqual(address.country, "Finland", "Testing address model")
        self.assertEqual(address.postal_code, 12345)
        self.assertEqual(address.town, "Tampere")
        self.assertEqual(address.street, "Main Street")
        self.assertEqual(address.street_number, 1)


class FriendshipTestCase(TestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam',
                                        email='adam@web.de',
                                        password='adamweb',
                                        )
        eva = User.objects.create_user(username='eva',
                                       email='eva@web.de',
                                       password='evaweb',
                                       )
        Friendship.objects.create(sender=adam,
                                  recipient=eva,
                                  status='request',
                                  )

    def test_friendship_is_setup(self):
        friendship = Friendship.objects.get(status="request")
        self.assertEqual(friendship.request_datetime.date(), datetime.datetime.now().date())
        self.assertEqual(friendship.response_datetime, None)
        self.assertEqual(friendship.sender.username, "adam")
        self.assertEqual(friendship.recipient.username, "eva")
        self.assertEqual(friendship.status, "request")


class StatusTestCase(TestCase):
    def setUp(self):
        FriendshipTestCase.setUp(self)
        adam = User.objects.get(username="adam")
        Status.objects.create(owner=adam,
                              title='FirstStatus',
                              message='blabla',
                              )

    def test_status_is_setup(self):
        status = Status.objects.get(title="FirstStatus")
        self.assertEqual(status.owner.username, "adam")
        self.assertEqual(status.message, "blabla")


class StatusCommentTestCase(TestCase):
    def setUp(self):
        StatusTestCase.setUp(self)
        status = Status.objects.get(title="FirstStatus")
        eva = User.objects.get(username="eva")
        Status_Comment.objects.create(message='statuscomment',
                                      user=eva,
                                      status=status,
                                      )

    def test_status_comment_is_setup(self):
        eva = User.objects.get(username="eva")
        status = Status.objects.get(title="FirstStatus")
        status_comment = Status_Comment.objects.get(message="statuscomment")
        self.assertEqual(status_comment.user, eva)
        self.assertEqual(status_comment.status, status)
