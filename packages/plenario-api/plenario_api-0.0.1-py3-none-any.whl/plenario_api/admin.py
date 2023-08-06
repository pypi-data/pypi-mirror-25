from django.contrib import admin
from plenario_core import admin as pcadmin

from .models import ShapeMeta, EtlEventMeta, StreamingEventMeta, \
    EtlSensorNetEventMeta, StreamingSensorNetEventMeta


admin.site.register(ShapeMeta, pcadmin.ShapeMetaBaseAdmin)
admin.site.register(EtlEventMeta, pcadmin.EtlEventMetaBaseAdmin)
admin.site.register(StreamingEventMeta, pcadmin.StreamingEventMetaBaseAdmin)
admin.site.register(EtlSensorNetEventMeta, pcadmin.EtlSensorNetEventMetaBaseAdmin)
admin.site.register(StreamingSensorNetEventMeta, pcadmin.StreamingSensorNetEventMetaBaseAdmin)
