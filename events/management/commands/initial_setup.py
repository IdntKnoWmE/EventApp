"""Management Command to setup the root domain, root tenant and the superuser."""

import logging
import random
import string

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone

from events.helper import get_cities
from events.models import Event, UserInterest, EventRating

# Only relevant once the Django project has started

User = get_user_model()


class Command(BaseCommand):
    help = """Creates Events raw data for setting up the project
           """
    cities = get_cities()

    def handle(self, *args, **options):
        # create your own events data

        logging.info('Process for data creation has started.')

        for _ in range(10):

            user, created = User.objects.get_or_create(
                first_name=self.random_string_gen(5),
                last_name=self.random_string_gen(5),
                email=f'{self.random_string_gen(4)}@{self.random_string_gen(4)}.com',
                password=self.get_random_password(),
                city=self.get_random_city()
            )

            logging.info(f'user is created with email: {user.email} and password: {user.email}')

            for _ in range(5):
                event, created = Event.objects.get_or_create(
                    title=self.random_string_gen(10),
                    description=self.random_string_gen(100),
                    city=self.get_random_city(),
                    date=self.get_random_date()
                )

                logging.info(f'event is created with city: {event.city} on date: {event.date}')

                if random.choice([True, False]):

                    user_interest = UserInterest.objects.create(
                        user=user,
                        event=event
                    )

                    logging.info(f'User: {user.email} has shown interest in event with {event.title}')

                if random.choice([True, False]):
                    event_rating = EventRating.objects.create(
                        user=user,
                        event=event,
                        rating=random.randint(1, 10)
                    )

                    logging.info(f'User has rated event with {event_rating.rating}')


    @staticmethod
    def random_string_gen(size):
        return ''.join(random.choices(string.ascii_lowercase, k=size))

    @staticmethod
    def get_random_city():

        cities = Command.cities
        total_city = len(cities)

        return cities[random.randint(0, total_city - 1)]

    @staticmethod
    def get_random_date():
        today = timezone.now()
        random_days = random.randint(0, 150)
        return today + timezone.timedelta(days=random_days)

    @staticmethod
    def get_random_password():

        cap_part = ''.join(random.choices(string.ascii_uppercase, k=2))
        low_part = ''.join(random.choices(string.ascii_lowercase, k=4))
        digit_part = ''.join(random.choices(string.digits, k=2))
        punc_part = ''.join(random.choices(string.punctuation, k=1))

        return cap_part + low_part + digit_part + punc_part
