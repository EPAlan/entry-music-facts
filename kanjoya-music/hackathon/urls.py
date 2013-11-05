from django.conf.urls import patterns, include, url
import myapp.views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackathon.views.home', name='home'),
    # url(r'^hackathon/', include('hackathon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^me/(\d)', myapp.views.addFact),
    url(r'^welcome/(\d)', myapp.views.trivia),
    url(r'^ajax/addFact', myapp.views.ajaxAddFact),
    url(r'^showAnswer', myapp.views.showAnswer),
    url(r'^uploadFile/(\d)', myapp.views.uploadFileView),
    url(r'^uploadAction/(\d)', myapp.views.uploadFile),
    (r'^$', myapp.views.index)


)