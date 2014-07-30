from django.conf.urls import patterns, include, url

from photolog.views import HomeView, PhotologDetailView, PhotologAsGalleryDetailView, \
                           PhotoCommentsView, NeedLoginView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^p/(?P<pk>\d+)/$', PhotologDetailView.as_view(), name='photolog-detail'),
    url(r'p/comment/(?P<pk>\d+)/$', PhotoCommentsView.as_view(), name='photo-comments'),
    url(r'^gallery/(?P<pk>\d+)/$', PhotologAsGalleryDetailView.as_view(), name='photolog-as-gallery-detail'),
    url(r'^update-photo-caption/$', 'photolog.views.update_photo_caption'),
    url(r'^hide-photo/$', 'photolog.views.hide_photo'),
    url(r'^rotation-photo/$', 'photolog.views.rotation_photo'),
    url(r'needlogin/$', NeedLoginView.as_view(), name='need-login'),
    url(r'get-comments/$', 'photolog.views.get_comments'),
    #url(r'^teststream/$', 'photolog.views.test_stream'),
    url(r'^checkphoto/$', 'photolog.views.stream_response'),
)
