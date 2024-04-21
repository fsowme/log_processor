from functools import partial

from factory import Faker

FakeDateTimeBetween = partial(Faker, provider='date_time_between')
