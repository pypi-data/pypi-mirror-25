import json
from random import choice, uniform

import arrow
from channels.test import ChannelTestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon
from django.core.urlresolvers import reverse
from moto import mock_s3
from plenario_core.utils import field_parsing as fp
from psycopg2.extras import DateTimeTZRange

from plenario_exporter_s3.models import ExportJob

from tests.app.models import EtlEventMeta


User = get_user_model()


class TestServices(ChannelTestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='test@example.com', password='shh secret')

        src_fields, _ = fp.deserialize_source_fields({
            'name': 'text',
            'lat': 'decimal',
            'long': 'decimal',
            'date': 'date',
        })
        pt_fields, _ = fp.deserialize_configured_point_fields([
            {'latitude': 'lat', 'longitude': 'long'}
        ])
        max_long, min_long = 12.76543, 12.34567
        max_lat, min_lat = 23.87654, 23.45678
        self.bbox = Polygon([
            [max_long, max_lat],
            [min_long, max_lat],
            [min_long, min_lat],
            [max_long, min_lat],
            [max_long, max_lat]
        ])
        self.meta_0 = EtlEventMeta.objects.create(
            name='test 0',
            contributor=self.user,
            source_url='https://example.com/0.csv',
            ds_source_fields=src_fields,
            ds_configured_point_fields=pt_fields,
            ds_bbox=self.bbox,
            ds_timerange=DateTimeTZRange(
                lower=arrow.utcnow().shift(hours=-1).datetime,
                upper=arrow.utcnow().shift(hours=+1).datetime
            )
        )
        self.meta_0.approve()
        self.meta_0.create_data_set_table()

        self.ds_model = self.meta_0.get_ds_model()

        for idx in range(10):
            name = f'row {idx}'
            long = uniform(min_long, max_long)
            lat = uniform(min_lat, max_lat)
            date = arrow.utcnow().shift(hours=choice(range(-1, 1))).datetime
            self.ds_model.objects.create(name=name, long=long, lat=lat, date=date)

    def tearDown(self):
        self.meta_0.delete()
        self.user.delete()

    @mock_s3
    def test_create_models_and_start_job(self):
        payload = json.dumps({
            'email_address': self.user.email,
            'ds_timerange': {
                'lower': arrow.utcnow().shift(hours=-2).datetime.isoformat(),
                'upper': arrow.utcnow().shift(hours=+2).datetime.isoformat()
            },
            'ds_bbox': json.loads(self.bbox.geojson),
            'data_sets': [
                {
                    'type': self.meta_0.__class__.__name__,
                    'pk': self.meta_0.pk,
                    'filter_point_field': '_meta_point_0',
                    'filter_date_field': 'date',
                }
            ]
        })
        url = reverse('export-meta')
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200, response.content)

        body = json.loads(response.content)
        self.assertIn('job_id', body)

        job_id = body['job_id']
        job = ExportJob.objects.get(pk=job_id)
        self.assertEqual(job.state, 'processing')
