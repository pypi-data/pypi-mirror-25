import random

import arrow
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon
from django.test import TestCase
from plenario_core.enums import RefreshRate
from psycopg2.extras import DateTimeTZRange

from plenario_api.models import ShapeMeta, EtlEventMeta, StreamingEventMeta, \
    EtlSensorNetEventMeta, StreamingSensorNetEventMeta


User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.chicago_bbox = Polygon([
            [
                -87.95242309570312,
                41.58155237169248
            ],
            [
                -87.52395629882812,
                41.58155237169248
            ],
            [
                -87.52395629882812,
                42.052351854553024
            ],
            [
                -87.95242309570312,
                42.052351854553024
            ],
            [
                -87.95242309570312,
                41.58155237169248
            ]
        ])
        cls.new_york_bbox = Polygon([
            [
                -74.300537109375,
                40.48873742102282
            ],
            [
                -73.4490966796875,
                40.48873742102282
            ],
            [
                -73.4490966796875,
                40.950862628132775
            ],
            [
                -74.300537109375,
                40.950862628132775
            ],
            [
                -74.300537109375,
                40.48873742102282
            ]
        ])
        cls.eastern_us_bbox = Polygon([
            [
                -95.97656249999999,
                24.44714958973082
            ],
            [
                -67.8515625,
                24.44714958973082
            ],
            [
                -67.8515625,
                48.28319289548349
            ],
            [
                -95.97656249999999,
                48.28319289548349
            ],
            [
                -95.97656249999999,
                24.44714958973082
            ]
        ])

        cls.timerange_2015 = DateTimeTZRange(
            lower=arrow.get(2015, 1, 1, 0, 0, 0).datetime,
            upper=arrow.get(2015, 12, 31, 23, 59, 59).datetime
        )
        cls.timerange_2016 = DateTimeTZRange(
            lower=arrow.get(2016, 1, 1, 0, 0, 0).datetime,
            upper=arrow.get(2016, 12, 31, 23, 59, 59).datetime
        )
        cls.timerange_2017 = DateTimeTZRange(
            lower=arrow.get(2017, 1, 1, 0, 0, 0).datetime,
            upper=arrow.get(2017, 12, 31, 23, 59, 59).datetime
        )

        cls.simple_source_fields = {
            'name': 'text',
            'location': 'text',
            'date': 'date',
        }
        cls.simple_point_fields = [
            {'coordinates': 'location'},
        ]
        cls.simple_date_fields = []

        cls.complicated_source_fields = {
            'name': 'text',
            'long': 'decimal',
            'lat': 'decimal',
            'year': 'integer',
            'month': 'integer',
            'day': 'integer',
            'hour': 'integer',
            'minute': 'integer',
            'seconds': 'integer',
        }
        cls.complicated_point_fields = [
            {
                'longitude': 'long',
                'latitude': 'lat'
            }
        ]
        cls.complicated_date_fields = [
            {
                'year': 'year',
                'month': 'month',
                'day': 'day',
                'hour': 'hour',
                'minute': 'minute',
                'second': 'second',
            }
        ]

    def setUp(self):
        self.user = User.objects.create(
            username='test', email='test@example.com', password='shh secret'
        )

        self._meta_base_kwargs = {
            'contributor': self.user.email,
            'description': 'this is a test',
            'attribution': 'vince',
        }
        self._etl_mixin_kwargs = {
            'refresh_rate': RefreshRate.Days.value,
            'refresh_interval': 1,
            'refresh_starts_on': None,
        }
        self._streaming_mixin_kwargs = {
            'is_relayed': True
        }
        self._geo_mixin_kwargs = {
            'ds_bbox': None,
        }
        self._time_mixin_kwargs = {
            'ds_timezone': 'UTC',
            'ds_timerange': None,
        }
        self._sensor_mixin_kwargs = {
            'nodes': [],
        }

    def tearDown(self):
        self.user.delete()

    def generate_random_name(self):
        num = random.choice(range(9999999))
        return f'test {num}'

    def generate_random_url(self):
        num = random.choice(range(9999999))
        return f'https://example.com/{num}.csv'

    def generate_chicago_coords(self):
        long_min, long_max = -87.52395629882812, -87.95242309570312
        lat_min, lat_max = 41.58155237169248, 42.052351854553024
        long = random.uniform(long_min, long_max)
        lat = random.uniform(lat_min, lat_max)
        return long, lat

    def generate_new_york_coords(self):
        long_min, long_max = -73.4490966796875, -74.300537109375
        lat_min, lat_max = 40.48873742102282, 40.950862628132775
        long = random.uniform(long_min, long_max)
        lat = random.uniform(lat_min, lat_max)
        return long, lat

    def generate_eastern_us_coords(self):
        long_min, long_max = -67.8515625, -95.97656249999999
        lat_min, lat_max = 24.44714958973082, 48.28319289548349
        long = random.uniform(long_min, long_max)
        lat = random.uniform(lat_min, lat_max)
        return long, lat

    def generate_2015_datetime(self):
        hours = random.choice(range(-5000, 5000))
        return arrow.utcnow().shift(hours=hours).replace(year=2015).datetime

    def generate_2016_datetime(self):
        hours = random.choice(range(-5000, 5000))
        return arrow.utcnow().shift(hours=hours).replace(year=2016).datetime

    def generate_2017_datetime(self):
        hours = random.choice(range(-5000, 5000))
        return arrow.utcnow().shift(hours=hours).replace(year=2017).datetime

    def generate_shape_meta(self):
        return ShapeMeta.objects.create(
            **self._meta_base_kwargs,
            **self._etl_mixin_kwargs,
            **self._geo_mixin_kwargs
        )

    def generate_etl_event_meta(self):
        return EtlEventMeta.objects.create(
            **self._meta_base_kwargs,
            **self._etl_mixin_kwargs,
            **self._time_mixin_kwargs,
            **self._geo_mixin_kwargs
        )

    def generate_streaming_event_meta(self):
        return StreamingEventMeta.objects.create(
            **self._meta_base_kwargs,
            **self._streaming_mixin_kwargs,
            **self._time_mixin_kwargs,
            **self._geo_mixin_kwargs
        )

    def generate_etl_sensor_meta(self):
        return EtlSensorNetEventMeta.objects.create(
            **self._meta_base_kwargs,
            **self._etl_mixin_kwargs,
            **self._time_mixin_kwargs,
            **self._geo_mixin_kwargs,
            **self._sensor_mixin_kwargs
        )

    def generate_streaming_sensor_meta(self):
        return StreamingSensorNetEventMeta.objects.create(
            **self._meta_base_kwargs,
            **self._streaming_mixin_kwargs,
            **self._time_mixin_kwargs,
            **self._geo_mixin_kwargs,
            **self._sensor_mixin_kwargs
        )
