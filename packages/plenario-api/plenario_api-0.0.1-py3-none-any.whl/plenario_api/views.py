from plenario_core import deserializers, serializers
from plenario_core.views import export, meta_generic, search
from plenario_exporter_s3 import services

from .models import ShapeMeta, EtlEventMeta, StreamingEventMeta, \
    EtlSensorNetEventMeta, StreamingSensorNetEventMeta


# shapefiles
_shape_view_kwargs = {
    'model': ShapeMeta,
    'manager': ShapeMeta.ready_objects,
    'serializer': serializers.ShapeMetaBaseSerializer(),
    'deserializer': deserializers.ShapeMetaBaseDeserializer()
}
fetch_shape_meta = meta_generic.GenericMetaFetchView.as_view(**_shape_view_kwargs)
list_shape_metas = meta_generic.GenericMetaListView.as_view(**_shape_view_kwargs)
create_shape_meta = meta_generic.GenericMetaCreateView.as_view(**_shape_view_kwargs)
update_shape_meta = meta_generic.GenericMetaUpdateView.as_view(**_shape_view_kwargs)
delete_shape_meta = meta_generic.GenericMetaDeleteView.as_view(**_shape_view_kwargs)

# etl event
_etl_event_view_kwargs = {
    'model': EtlEventMeta,
    'manager': EtlEventMeta.ready_objects,
    'serializer': serializers.EtlEventMetaBaseSerializer(),
    'deserializer': deserializers.EtlEventMetaBaseDeserializer()
}
fetch_etl_event_meta = meta_generic.GenericMetaFetchView.as_view(**_etl_event_view_kwargs)
list_etl_event_metas = meta_generic.GenericMetaListView.as_view(**_etl_event_view_kwargs)
create_etl_event_meta = meta_generic.GenericMetaCreateView.as_view(**_etl_event_view_kwargs)
update_etl_event_meta = meta_generic.GenericMetaUpdateView.as_view(**_etl_event_view_kwargs)
delete_etl_event_meta = meta_generic.GenericMetaDeleteView.as_view(**_etl_event_view_kwargs)

# streaming event
_streaming_event_view_kwargs = {
    'model': StreamingEventMeta,
    'manager': StreamingEventMeta.ready_objects,
    'serializer': serializers.StreamingEventMetaBaseSerializer(),
    'deserializer': deserializers.StreamingEventMetaBaseDeserializer()
}
fetch_streaming_event_meta = meta_generic.GenericMetaFetchView.as_view(**_streaming_event_view_kwargs)
list_streaming_event_metas = meta_generic.GenericMetaListView.as_view(**_streaming_event_view_kwargs)
create_streaming_event_meta = meta_generic.GenericMetaCreateView.as_view(**_streaming_event_view_kwargs)
update_streaming_event_meta = meta_generic.GenericMetaUpdateView.as_view(**_streaming_event_view_kwargs)
delete_streaming_event_meta = meta_generic.GenericMetaDeleteView.as_view(**_streaming_event_view_kwargs)

# etl sensor
_etl_sensor_view_kwargs = {
    'model': EtlSensorNetEventMeta,
    'manager': EtlSensorNetEventMeta.ready_objects,
    'serializer': serializers.EtlSensorNetEventMetaBaseSerializer(),
    'deserializer': deserializers.EtlSensorNetEventMetaBaseDeserializer()
}
fetch_etl_sensor_meta = meta_generic.GenericMetaFetchView.as_view(**_etl_sensor_view_kwargs)
list_etl_sensor_metas = meta_generic.GenericMetaListView.as_view(**_etl_sensor_view_kwargs)
create_etl_sensor_meta = meta_generic.GenericMetaCreateView.as_view(**_etl_sensor_view_kwargs)
update_etl_sensor_meta = meta_generic.GenericMetaUpdateView.as_view(**_etl_sensor_view_kwargs)
delete_etl_sensor_meta = meta_generic.GenericMetaDeleteView.as_view(**_etl_sensor_view_kwargs)

# streaming sensor
_streaming_sensor_view_kwargs = {
    'model': StreamingSensorNetEventMeta,
    'manager': StreamingSensorNetEventMeta.ready_objects,
    'serializer': serializers.StreamingSensorNetEventMetaBaseSerializer(),
    'deserializer': deserializers.StreamingSensorNetEventMetaBaseDeserializer()
}
fetch_streaming_sensor_meta = meta_generic.GenericMetaFetchView.as_view(**_streaming_sensor_view_kwargs)
list_streaming_sensor_metas = meta_generic.GenericMetaListView.as_view(**_streaming_sensor_view_kwargs)
create_streaming_sensor_meta = meta_generic.GenericMetaCreateView.as_view(**_streaming_sensor_view_kwargs)
update_streaming_sensor_meta = meta_generic.GenericMetaUpdateView.as_view(**_streaming_sensor_view_kwargs)
delete_streaming_sensor_meta = meta_generic.GenericMetaDeleteView.as_view(**_streaming_sensor_view_kwargs)

# search
search_metas = search.GenericMetaSearchView.as_view(
    manager_map={
        ShapeMeta: ShapeMeta.ready_objects,
        EtlEventMeta: EtlEventMeta.ready_objects,
        StreamingEventMeta: StreamingEventMeta.ready_objects,
        EtlSensorNetEventMeta: EtlSensorNetEventMeta.ready_objects,
        StreamingSensorNetEventMeta: StreamingSensorNetEventMeta.ready_objects,
    },
    serializer_map={
        ShapeMeta: serializers.ShapeMetaBaseSerializer(),
        EtlEventMeta: serializers.EtlEventMetaBaseSerializer(),
        StreamingEventMeta: serializers.StreamingEventMetaBaseSerializer(),
        EtlSensorNetEventMeta: serializers.EtlSensorNetEventMetaBaseSerializer(),
        StreamingSensorNetEventMeta: serializers.StreamingSensorNetEventMetaBaseSerializer(),
    }
)

# export view
export_metas = export.GenericMetaExportView.as_view(
    models=[ShapeMeta, EtlEventMeta, StreamingEventMeta, EtlSensorNetEventMeta, StreamingSensorNetEventMeta],
    async_handler=services.create_models_and_start_job
)
