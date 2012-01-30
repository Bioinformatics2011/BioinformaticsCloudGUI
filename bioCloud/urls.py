from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bioCloud.views.home', name='home'),
    # url(r'^bioCloud/', include('bioCloud.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^biocloud/$', 'biocloud.views.index'),
    url(r'^workflow/$', 'biocloud.views.workflow'),
    url(r'^xhr/createProjectFolder$', 'biocloud.views.xhr_createProjectFolder'),
    url(r'^xhr/xhr_upload/$', "biocloud.views.xhr_upload", name="xhr_upload"),
    url(r'^xhr/([^/|]+)/content$', 'biocloud.views.xhr_folderContents')
)
