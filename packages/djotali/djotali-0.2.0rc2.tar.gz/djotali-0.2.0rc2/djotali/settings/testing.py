# coding: utf-8
from .base import *

FIXTURE_DIRS = [os.path.join(BASE_DIR, 'tests/djotali/fixtures/'), ]
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///dev.sqlite3', conn_max_age=600)
}
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
CELERY_RESULT_BACKEND = 'db+sqlite:///test.sqlite3'

if not os.path.isdir('data'):
    os.mkdir('data')
REDIS_DB_PATH = os.path.join('data/test_redis.db')
rdb = Redis(REDIS_DB_PATH)
REDIS_SOCKET_PATH = 'redis+socket://%s' % (rdb.socket_file,)
CELERY_BROKER_URL = REDIS_SOCKET_PATH
