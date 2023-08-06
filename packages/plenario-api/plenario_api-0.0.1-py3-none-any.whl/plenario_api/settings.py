import os

# app configs
PLENARIO_APPS = [
    'channels',
    'plenario_core',
    'plenario_mailer_core',
    'plenario_exporter_s3',
    'plenario_api',
]

# exporter configs
PLENARIO_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        'ROUTING': 'plenario_exporter_s3.routing.channel_routing',
    },
}


# mailer configs
PLENARIO_ADMINS = [
    ('Plenario Admins', 'plenario@lists.uchicago.edu'),
]
