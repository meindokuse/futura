from celery import Celery, signals

from src.config import REDIS_URL
from src.db.cache import init_sync_redis, close_sync_redis

app = Celery(
    'celery_app',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        'src.celery.tasks.redis_update_task',
        'src.celery.tasks.bot_send_task',
    ]
)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=8,
    task_default_queue='default',
    broker_transport_options={'visibility_timeout': 3600}
)


@signals.worker_process_init.connect
def worker_init(**kwargs):
    init_sync_redis()


@signals.worker_process_shutdown.connect
def worker_shutdown(**kwargs):
    close_sync_redis()
