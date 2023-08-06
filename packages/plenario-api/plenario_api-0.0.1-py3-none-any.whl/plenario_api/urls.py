from django.conf.urls import url

from . import views


urlpatterns = [
    # search
    url(
        regex=r'^meta-data/search',
        view=views.search_metas,
        name='search-metas'
    ),

    # export
    url(
        regex=r'^meta-data/export',
        view=views.export_metas,
        name='export-metas'
    ),

    # shapefiles
    url(
        regex=r'^meta-data/shapefiles/(?P<pk>\d+)/fetch',
        view=views.fetch_shape_meta,
        name='fetch-shape-meta'
    ),
    url(
        regex=r'^meta-data/shapefiles/list',
        view=views.list_shape_metas,
        name='list-shape-metas'
    ),
    url(
        regex=r'^meta-data/shapefiles/create',
        view=views.create_shape_meta,
        name='create-shape-meta'
    ),
    url(
        regex=r'^meta-data/shapefiles/(?P<pk>\d+)/update',
        view=views.update_shape_meta,
        name='update-shape-meta'
    ),
    url(
        regex=r'^meta-data/shapefiles/(?P<pk>\d+)/delete',
        view=views.delete_shape_meta,
        name='delete-shape-meta'
    ),

    # etl events
    url(
        regex=r'^meta-data/etl-events/(?P<pk>\d+)/fetch',
        view=views.fetch_etl_event_meta,
        name='fetch-etl-event-meta'
    ),
    url(
        regex=r'^meta-data/etl-events/list',
        view=views.list_etl_event_metas,
        name='list-etl-event-metas'
    ),
    url(
        regex=r'^meta-data/etl-events/create',
        view=views.create_etl_event_meta,
        name='create-etl-event-meta'
    ),
    url(
        regex=r'^meta-data/etl-events/(?P<pk>\d+)/update',
        view=views.update_etl_event_meta,
        name='update-etl-event-meta'
    ),
    url(
        regex=r'^meta-data/etl-events/(?P<pk>\d+)/delete',
        view=views.delete_etl_event_meta,
        name='delete-etl-event-meta'
    ),

    # streaming events
    url(
        regex=r'^meta-data/streaming-events/(?P<pk>\d+)/fetch',
        view=views.fetch_streaming_event_meta,
        name='fetch-streaming-event-meta'
    ),
    url(
        regex=r'^meta-data/streaming-events/list',
        view=views.list_streaming_event_metas,
        name='list-streaming-event-metas'
    ),
    url(
        regex=r'^meta-data/streaming-events/create',
        view=views.create_streaming_event_meta,
        name='create-streaming-event-meta'
    ),
    url(
        regex=r'^meta-data/streaming-events/(?P<pk>\d+)/update',
        view=views.update_streaming_event_meta,
        name='update-streaming-event-meta'
    ),
    url(
        regex=r'^meta-data/streaming-events/(?P<pk>\d+)/delete',
        view=views.delete_streaming_event_meta,
        name='delete-streaming-event-meta'
    ),

    # etl sensors
    url(
        regex=r'^meta-data/etl-sensors/(?P<pk>\d+)/fetch',
        view=views.fetch_etl_sensor_meta,
        name='fetch-etl-sensor-meta'
    ),
    url(
        regex=r'^meta-data/etl-sensors/list',
        view=views.list_etl_sensor_metas,
        name='list-etl-sensor-metas'
    ),
    url(
        regex=r'^meta-data/etl-sensors/create',
        view=views.create_etl_sensor_meta,
        name='create-etl-sensor-meta'
    ),
    url(
        regex=r'^meta-data/etl-sensors/(?P<pk>\d+)/update',
        view=views.update_etl_sensor_meta,
        name='update-etl-sensor-meta'
    ),
    url(
        regex=r'^meta-data/etl-sensors/(?P<pk>\d+)/delete',
        view=views.delete_etl_sensor_meta,
        name='delete-etl-sensor-meta'
    ),

    # streaming sensors
    url(
        regex=r'^meta-data/streaming-sensors/(?P<pk>\d+)/fetch',
        view=views.fetch_streaming_sensor_meta,
        name='fetch-streaming-sensor-meta'
    ),
    url(
        regex=r'^meta-data/streaming-sensors/list',
        view=views.list_streaming_sensor_metas,
        name='list-streaming-sensor-metas'
    ),
    url(
        regex=r'^meta-data/streaming-sensors/create',
        view=views.create_streaming_sensor_meta,
        name='create-streaming-sensor-meta'
    ),
    url(
        regex=r'^meta-data/streaming-sensors/(?P<pk>\d+)/update',
        view=views.update_streaming_sensor_meta,
        name='update-streaming-sensor-meta'
    ),
    url(
        regex=r'^meta-data/streaming-sensors/(?P<pk>\d+)/delete',
        view=views.delete_streaming_sensor_meta,
        name='delete-streaming-sensor-meta'
    ),
]
