from django.test import TestCase
from users.models import User, Address, Friendship, Status, Status_Comment
from events.models import Place, Event
import datetime


# Create your tests here.


class PlaceTestCase(TestCase):
    def setUp(self):
        address = Address.objects.create(country="Finland",
                                         postal_code=12345,
                                         town="Tampere",
                                         street="Main Street",
                                         street_number=1,
                                         )
        Place.objects.create(name='place',
                             description='description',
                             address=address)

    def test_place_is_setup(self):
        place = Place.objects.get(name="place")
        self.assertEqual(place.description, "description")
        self.assertEqual(place.address.country, "Finland")


class EventTestCase(TestCase):
    startDate = datetime.datetime.now()
    endDate = startDate

    def setUp(self):
        PlaceTestCase.setUp(self)
        place = Place.objects.get(name="place")
        adam = User.objects.create_user(username='adam',
                                        email='adam@web.de',
                                        password='adamweb',
                                        )
        eva = User.objects.create_user(username='eva',
                                       email='eva@web.de',
                                       password='evaweb',
                                       )
        event = Event.objects.create(owner=adam,
                                     name='event',
                                     description='description',
                                     category='sitsit',
                                     start_datetime=EventTestCase.startDate,
                                     end_datetime=EventTestCase.endDate,
                                     #start_time=EventTestCase.startTime,
                                     #end_time=EventTestCase.endTime,
                                     place=place,
                                     )
        event.participants.add(eva)
        event.save()

    def test_event_is_setup(self):
        event = Event.objects.get(name="event")
        self.assertEqual(event.owner.username, "adam")
        self.assertEqual(event.description, "description")
        self.assertEqual(event.category, "sitsit")
        self.assertEqual(event.start_datetime.day, EventTestCase.startDate.day)
        self.assertEqual(event.end_datetime.day, EventTestCase.endDate.day)
        #self.assertEqual(event.start_time, EventTestCase.startTime)
        #self.assertEqual(event.end_time, EventTestCase.endTime)
        self.assertEqual(event.place.name, "place")