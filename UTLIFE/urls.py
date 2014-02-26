from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings


from model_report import report
report.autodiscover()

admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('UTLIFEapp.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^report/', include('model_report.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT,}),
)
