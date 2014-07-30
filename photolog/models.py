import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.signals import saved_file, thumbnail_created

from django.conf import settings

from photolog import settings

import qiniu.conf
import qiniu.rs

qiniu.conf.ACCESS_KEY = settings.QINIU_ACCESS_KEY
qiniu.conf.SECRET_KEY = settings.QINIU_SECRET_KEY

class Avatar(models.Model):
    title       = models.CharField(_('title'), max_length=256, blank=True)
    avatar      = ThumbnailerImageField(upload_to='avatars/%Y/%m/%d', resize_source=dict(size=(1600, 1600), quality=100))
    upload_date = models.DateTimeField(_('upload datetime'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('avatar')
        verbose_name_plural = _('avatars')

class SiteSettings(models.Model):
    site_title     = models.CharField(_('site title'), max_length=256)
    avatar         = models.ForeignKey(Avatar, verbose_name=_('avatar'))
    photolog_title = models.CharField(_('photolog title'), max_length=256)
    photolog_intro = models.TextField(_('photolog intro'), blank=True)

    def __unicode__(self):
        return self.site_title

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = verbose_name

class Entry(models.Model):
    title       = models.CharField(_('title'), max_length=256, blank=True)
    date        = models.DateField(_('date'), unique=True, db_index=True)
    content     = models.TextField(_('content'), blank=True)
    create_date = models.DateTimeField(_('create time'), auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ['-date']
        permissions = (
            ('edit_photologs', _('Can edit photologs and photos')),
        )

class Photo(models.Model):
    entry         = models.ForeignKey(Entry, verbose_name=_('entry'))
    title         = models.CharField(_('title'), max_length=256)
    photo         = ThumbnailerImageField(_('photo'), upload_to='photos/%Y/%m/%d', resize_source=dict(size=(1200, 1200), quality=100))
    upload_date   = models.DateTimeField(_('upload datetime'), auto_now_add=True, editable=False)
    caption       = models.TextField(_('caption'))
    shooting_time = models.DateTimeField(_('shooting time'), blank=True, null=True)
    md5_original  = models.CharField(_('md5 hash of original file'), max_length=64, blank=True)
    duplicate     = models.BooleanField(_('duplicate file'), default=False)
    hidden        = models.BooleanField(_('hide photo'), default=False)
    order         = models.IntegerField(_('order'), default=50)
    exif          = models.TextField(_('exif'), blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        ordering = ['order', '-shooting_time']

def update_qiniu(filefield):
    key = "media/" + filefield
    ret, err = qiniu.rs.Client().delete(settings.QINIU_BUCKET_NAME, key)
    nowtime = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_file = open(settings.QINIU_LOG_FILE, 'a')
    if err is not None:
        log_file.write('%s error: %s. (%s)\n' % (nowtime, err, key))
    else:
        log_file.write('%s delete file: %s.\n' % (nowtime, key))
    log_file.close()

def update_qiniu_signal(sender, **kwargs):
    if sender:
        update_qiniu(str(sender))

thumbnail_created.connect(update_qiniu_signal)

_('Avatar')
_('SiteSettings')
_('Entry')
_('Photo')
