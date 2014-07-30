import random
import re
import time
import datetime
import os
import hashlib
import exifread
from PIL import Image as PilImage

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.http import StreamingHttpResponse, CompatibleStreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import permission_required
from django.core.files import File
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model

from django.conf import settings as dj_settings

from photolog import settings
from photolog.models import Entry, Photo, SiteSettings, update_qiniu

class HomeView(TemplateView):

    template_name = 'photolog/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['photologs'] = Entry.objects.all().order_by('-date')
        context['settings'] = SiteSettings.objects.all().latest('pk')
        context['random'] = random.uniform(0, 1)
        return context

class NeedLoginView(TemplateView):

    template_name = 'photolog/needlogin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super(NeedLoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NeedLoginView, self).get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.all().latest('pk')
        context['random'] = random.uniform(0, 1)
        return context

class PhotologDetailView(DetailView):

    model = Entry

    def get_context_data(self, **kwargs):
        context = super(PhotologDetailView, self).get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.all().latest('pk')
        context['random'] = random.uniform(0, 1)
        return context

class PhotologAsGalleryDetailView(DetailView):

    model = Entry
    template_name = 'photolog/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(PhotologAsGalleryDetailView, self).get_context_data(**kwargs)
        context['settings'] = SiteSettings.objects.all().latest('pk')
        context['random'] = random.uniform(0, 1)
        return context

def get_file_md5(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def get_photo_exif(filename):
    return exifread.process_file(open(filename, 'rb'))

"""
def test_stream(request):
    response = StreamingHttpResponse(test_stream_response())
    response['X-Accel-Buffering'] = 'no'
    return response

def test_stream_response():
    for x in range(1,11):
        yield "%s\n\n<br />" % x
        print x
        time.sleep(1)
"""

@permission_required('is_superuser', raise_exception=True)
def stream_response(request):
    response = StreamingHttpResponse(stream_response_generator())
    response['X-Accel-Buffering'] = 'no'
    return response

def stream_response_generator():
    files = os.listdir(settings.WATCH_DIR)

    yield '<!DOCTYPE html>\n'
    yield '<html lang="zh-cn">\n'
    yield '<head><style>\n'
    yield '*{padding:0;margin:0;border:0;}\n'
    yield 'body{font-size:14px;background:#ececec;line-height:1.5em;}\n'
    yield '#wrap{width:900px;margin:0 auto;}\n'
    yield '</style></head>\n'
    yield '<body><div id="wrap">\n'

    n = 0
    for f in files:
        n = n + 1
        filepath = settings.WATCH_DIR + os.sep + f
        exif = get_photo_exif(filepath)
        shooting_time = str(exif.get('EXIF DateTimeOriginal', ''))
        md5 = get_file_md5(filepath)
        photos_duplicate = Photo.objects.filter(md5_original=md5)
        duplicate = False
        if photos_duplicate:
            duplicate = True
        regex=ur'\d{4}:\d{2}:\d{2}'
        if shooting_time:
            match = re.search(regex, shooting_time)
            if match:
                shooting_date = datetime.datetime.strptime(match.group(), '%Y:%m:%d').date()
            else:
                shooting_date = datetime.date.today()
        else:
            shooting_date = datetime.date.today()

        entry, created = Entry.objects.get_or_create(date=shooting_date)
        if created:
            entry.title = shooting_date
            entry.save()

        photofile = open(filepath)
        photo = Photo()
        photo.entry = entry
        photo.title = f
        photo.photo = File(photofile)
        photo.caption = f
        photo.exif = exif
        if shooting_time:
            try:
                photo.shooting_time = datetime.datetime.strptime(shooting_time, '%Y:%m:%d %H:%M:%S')
            except:
                pass
        photo.md5_original = md5
        photo.duplicate = duplicate
        photo.save()
        photofile.close()
        yield "<p>%s. Saving photo: %s, shooting time: %s</p>" % (n, f, shooting_time)

    yield '<p>done!</p>\n'
    yield '</div></body></html>'

@csrf_exempt
def update_photo_caption(request):
    if request.method == 'POST' and request.user.has_perm('photolog.edit_photologs'):
        data = request.POST
        photo = get_object_or_404(Photo, pk=data['id'])
        if data['caption']:
            photo.caption = data['caption']
            photo.save()
            return HttpResponse(photo.caption)
        else:
            return HttpResponse(1)
    else:
        return HttpResponse(2)

@csrf_exempt
def hide_photo(request):
    if request.method == 'POST' and request.user.has_perm('photolog.edit_photologs'):
        pid = request.POST.get('id', '')
        if pid:
            photo = get_object_or_404(Photo, pk=pid)
            if photo.hidden:
                photo.hidden = False
            else:
                photo.hidden = True
            photo.save()
            return HttpResponse(photo.photo['list'].url)

@csrf_exempt
def rotation_photo(request):
    if request.method == 'POST' and request.user.has_perm('photolog.edit_photologs'):
        direction = request.POST.get('r', 'n')
        pid = request.POST.get('id', '')
        if pid:
            photo = get_object_or_404(Photo, pk=pid)
            if direction == 's':
                degrees = -90
            else:
                degrees = 90
            im = PilImage.open(photo.photo.path)

            rotated_image = im.rotate(degrees)

            rotated_image.save(photo.photo.path, overwrite=True)

            # update qiniu
            if 'qiniudn' in dj_settings.MEDIA_URL:
                update_qiniu(str(photo.photo))

            # create new image
            new_image_url = photo.photo['list'].url

            return HttpResponse(1)

class PhotoCommentsView(TemplateView):

    template_name = "photolog/photo_comments.html"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PhotoCommentsView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        photo = get_object_or_404(Photo, pk=pk)
        context['object'] = photo
        return context

def get_comments(request):
    ctype = request.GET.get('ctype', '')
    object_pk = request.GET.get('object_pk', '')
    template_name = "photolog/get_comments_ajax.html"

    if ctype and object_pk:
        app, model = ctype.split('.')
        obj = get_object_or_404(get_model(app, model), pk=object_pk)

        context = RequestContext(request)
        return render_to_response(template_name, {'object': obj}, context)
