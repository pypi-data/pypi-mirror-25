"""
this will simulate a workflow --

1. create metas via the api
2. metas approved and tables created via the models (would be an admin action)
3. load some dummy data for the data sets (would be an etl/stream action)
4. search the models
5. request export of the models
"""

import json
from copy import copy

from django.core.urlresolvers import reverse
from moto import mock_s3

from .bases import BaseTest
from plenario_api.models import ShapeMeta, EtlEventMeta, StreamingEventMeta, \
    EtlSensorNetEventMeta, StreamingSensorNetEventMeta


class TestIntegrationViaWorkflow(BaseTest):

    @mock_s3
    def test_workflow(self):
        json_ct = 'application/json'

        # create metas
        for idx in range(3):
            payload = {
                'name': self.generate_random_name(),
                'source_url': self.generate_random_url(),
                'ds_source_fields': copy(self.simple_source_fields),
                'ds_configured_point_fields': self.simple_point_fields,
            }
            del payload['ds_source_fields']['date']
            payload.update(self._meta_base_kwargs)
            payload.update(self._etl_mixin_kwargs)
            payload.update(self._geo_mixin_kwargs)

            payload = json.dumps(payload)
            url = reverse('api:create-shape-meta')
            response = self.client.post(url, payload, content_type=json_ct)
            self.assertEqual(response.status_code, 201, response.content)
        for _ in range(3):
            payload = {
                'name': self.generate_random_name(),
                'source_url': self.generate_random_url(),
                'ds_source_fields': self.simple_source_fields,
                'ds_configured_point_fields': self.simple_point_fields,
            }
            payload.update(self._meta_base_kwargs)
            payload.update(self._etl_mixin_kwargs)
            payload.update(self._geo_mixin_kwargs)
            payload.update(self._time_mixin_kwargs)

            payload = json.dumps(payload)
            url = reverse('api:create-etl-event-meta')
            response = self.client.post(url, payload, content_type=json_ct)
            self.assertEqual(response.status_code, 201, response.content)
        for _ in range(3):
            payload = {
                'name': self.generate_random_name(),
                'ds_source_fields': self.simple_source_fields,
                'ds_configured_point_fields': self.simple_point_fields,
            }
            payload.update(self._meta_base_kwargs)
            payload.update(self._streaming_mixin_kwargs)
            payload.update(self._geo_mixin_kwargs)
            payload.update(self._time_mixin_kwargs)

            payload = json.dumps(payload)
            url = reverse('api:create-streaming-event-meta')
            response = self.client.post(url, payload, content_type=json_ct)
            self.assertEqual(response.status_code, 201, response.content)
        for _ in range(3):
            payload = {
                'name': self.generate_random_name(),
                'source_url': self.generate_random_url(),
                'ds_source_fields': self.simple_source_fields,
                'ds_configured_point_fields': self.simple_point_fields,
            }
            payload.update(self._meta_base_kwargs)
            payload.update(self._etl_mixin_kwargs)
            payload.update(self._geo_mixin_kwargs)
            payload.update(self._time_mixin_kwargs)
            payload.update(self._sensor_mixin_kwargs)

            payload = json.dumps(payload)
            url = reverse('api:create-etl-sensor-meta')
            response = self.client.post(url, payload, content_type=json_ct)
            self.assertEqual(response.status_code, 201, response.content)
        for _ in range(3):
            payload = {
                'name': self.generate_random_name(),
                'ds_source_fields': self.simple_source_fields,
                'ds_configured_point_fields': self.simple_point_fields,
            }
            payload.update(self._meta_base_kwargs)
            payload.update(self._streaming_mixin_kwargs)
            payload.update(self._geo_mixin_kwargs)
            payload.update(self._time_mixin_kwargs)
            payload.update(self._sensor_mixin_kwargs)

            payload = json.dumps(payload)
            url = reverse('api:create-streaming-sensor-meta')
            response = self.client.post(url, payload, content_type=json_ct)
            self.assertEqual(response.status_code, 201, response.content)

        # approve the metas and create their data bases
        for model in ShapeMeta.objects.all():
            model.approve()
            model.create_data_set_table()
            model.save()
        for model in EtlEventMeta.objects.all():
            model.approve()
            model.create_data_set_table()
            model.save()
        for model in StreamingEventMeta.objects.all():
            model.approve()
            model.create_data_set_table()
            model.save()
        for model in EtlSensorNetEventMeta.objects.all():
            model.approve()
            model.create_data_set_table()
            model.save()
        for model in StreamingSensorNetEventMeta.objects.all():
            model.approve()
            model.create_data_set_table()
            model.save()

        # assert the tables have been created
        for model in ShapeMeta.objects.all():
            ds_model = model.get_ds_model()
            ds_model.objects.all()
        for model in EtlEventMeta.objects.all():
            ds_model = model.get_ds_model()
            ds_model.objects.all()
        for model in StreamingEventMeta.objects.all():
            ds_model = model.get_ds_model()
            ds_model.objects.all()
        for model in EtlSensorNetEventMeta.objects.all():
            ds_model = model.get_ds_model()
            ds_model.objects.all()
        for model in StreamingSensorNetEventMeta.objects.all():
            ds_model = model.get_ds_model()
            ds_model.objects.all()

        # create some dummy data
        for model in ShapeMeta.objects.all():
            model.ds_bbox = self.chicago_bbox
            model.save()
            ds_model = model.get_ds_model()
            for idx in range(10):
                long, lat = self.generate_chicago_coords()
                ds_model.objects.create(
                    name=f'row {idx}',
                    location=f'{long},{lat}'
                )
        for model in EtlEventMeta.objects.all():
            model.ds_bbox = self.new_york_bbox
            model.ds_timerange = self.timerange_2016
            model.save()
            ds_model = model.get_ds_model()
            for idx in range(10):
                long, lat = self.generate_new_york_coords()
                ds_model.objects.create(
                    name=f'row {idx}',
                    location=f'{long},{lat}',
                    date=self.generate_2016_datetime()
                )
        for model in StreamingEventMeta.objects.all():
            model.ds_bbox = self.new_york_bbox
            model.ds_timerange = self.timerange_2016
            model.save()
            ds_model = model.get_ds_model()
            for idx in range(10):
                long, lat = self.generate_new_york_coords()
                ds_model.objects.create(
                    name=f'row {idx}',
                    location=f'{long},{lat}',
                    date=self.generate_2016_datetime()
                )
        for model in EtlSensorNetEventMeta.objects.all():
            model.ds_bbox = self.chicago_bbox
            model.ds_timerange = self.timerange_2017
            model.save()
            ds_model = model.get_ds_model()
            for idx in range(10):
                long, lat = self.generate_chicago_coords()
                ds_model.objects.create(
                    name=f'row {idx}',
                    location=f'{long},{lat}',
                    date=self.generate_2017_datetime()
                )
        for model in StreamingSensorNetEventMeta.objects.all():
            model.ds_bbox = self.chicago_bbox
            model.ds_timerange = self.timerange_2017
            model.save()
            ds_model = model.get_ds_model()
            for idx in range(10):
                long, lat = self.generate_chicago_coords()
                ds_model.objects.create(
                    name=f'row {idx}',
                    location=f'{long},{lat}',
                    date=self.generate_2017_datetime()
                )

        # search metas
        payload = json.dumps({
            'ds_bbox': json.loads(self.eastern_us_bbox.geojson),
            'ds_timerange': {
                'lower': '2015-01-01T00:00:00+00:00',
                'upper': '2018-01-01T00:00:00+00:00',
            }
        })
        url = reverse('api:search-metas')
        response = self.client.post(url, payload, content_type=json_ct)
        self.assertEqual(response.status_code, 200, response.content)

        search_body = json.loads(response.content)
        self.assertEqual(len(search_body), 15, search_body)

        # request export
        payload = {
            'email_address': self.user.email,
            'ds_bbox': json.loads(self.eastern_us_bbox.geojson),
            'ds_timerange': {
                'lower': '2015-01-01T00:00:00+00:00',
                'upper': '2018-01-01T00:00:00+00:00',
            },
            'data_sets': []
        }
        for details in search_body:
            payload['data_sets'].append({
                'type': details['type'],
                'pk': details['pk'],
                'filter_point_field': '_meta_point_0',
                'filter_date_field': 'date',
            })
        payload = json.dumps(payload)
        url = reverse('api:export-metas')
        response = self.client.post(url, payload, content_type=json_ct)
        self.assertEqual(response.status_code, 200, response.content)
