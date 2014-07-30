from django.conf import settings

WATCH_DIR = getattr(settings, 'WATCH_DIR', 'ftp')

QINIU_ACCESS_KEY = getattr(settings, 'QINIU_ACCESS_KEY', '')
QINIU_SECRET_KEY = getattr(settings, 'QINIU_SECRET_KEY', '')

QINIU_BUCKET_NAME = getattr(settings, 'QINIU_BUCKET_NAME', '')

QINIU_LOG_FILE = getattr(settings, 'QINIU_LOG_FILE', '')
