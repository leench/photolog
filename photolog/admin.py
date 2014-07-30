from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer

from tinymce.widgets import TinyMCE

from photolog.models import Avatar, SiteSettings, Entry, Photo

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'upload_date')
    list_display_links = ('admin_thumbnail', 'title')
    list_per_page = 30

    def admin_thumbnail(self, obj):
        return u'<img src="%s" />' % (obj.avatar['avatar'].url)
    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'create_date')
    inlines = [ PhotoInline, ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 20},
            ))
        return super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'caption', 'shooting_time', 'hidden', 'duplicate', 'upload_date')
    list_display_links = ('admin_thumbnail', 'title', )
    readonly_fields = ('exif', 'shooting_time', 'md5_original')
    list_per_page = 30

    def admin_thumbnail(self, obj):
        thumbnailer = get_thumbnailer(obj.photo)
        thumbnail_options = {
            'size': (90, 90),
            'crop': False,
        }
        return u'<img src="%s" />' % (thumbnailer.get_thumbnail(thumbnail_options).url)
        #return u'<img src="%s" />' % (obj.photo.url)
    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'caption':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 10},
            ))
        return super(PhotoAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Avatar, AvatarAdmin)
admin.site.register(SiteSettings)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Photo, PhotoAdmin)
