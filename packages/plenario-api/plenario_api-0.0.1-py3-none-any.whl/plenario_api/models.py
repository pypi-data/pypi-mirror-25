from django.db.models import permalink
from plenario_core import models


class ShapeMeta(models.ShapeMetaBase):
    @permalink
    def get_absolute_url(self):
        return 'api:fetch-shape-meta', [self.pk]


class EtlEventMeta(models.EtlEventMetaBase):
    @permalink
    def get_absolute_url(self):
        return 'api:fetch-etl-event-meta', [self.pk]


class StreamingEventMeta(models.StreamingEventMetaBase):
    @permalink
    def get_absolute_url(self):
        return 'api:fetch-streaming-event-meta', [self.pk]


class EtlSensorNetEventMeta(models.EtlSensorNetEventMetaBase):
    @permalink
    def get_absolute_url(self):
        return 'api:fetch-etl-sensor-meta', [self.pk]


class StreamingSensorNetEventMeta(models.StreamingSensorNetEventMetaBase):
    @permalink
    def get_absolute_url(self):
        return 'api:fetch-streaming-sensor-meta', [self.pk]
