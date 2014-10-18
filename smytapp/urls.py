from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^obj_create/(?P<mod_id>[a-zA-Z]+)/', 'app.views.obj_create'),
    url(r'^obj_update/(?P<mod_id>[a-zA-Z]+)/', 'app.views.obj_update'),
    url(r'^json_obj/(?P<mod_id>[a-zA-Z]+)/', 'app.views.json_obj'),
    url(r'^json_cls/', 'app.views.json_cls'),
    url(r'^$', 'app.views.index'),
)

