добавлены файлы celery и tasks для асинхронного выполнения почтовой рассылки.

Еженедельная рассылка теперь реализована через celery, а не через apscheduler.

Celery запускается в различных окнах через команды (для windows):

    celery -A NewsPaper worker -l INFO -P eventlet
    celery -A NewsPaper beat -l INFO