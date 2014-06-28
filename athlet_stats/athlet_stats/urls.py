from django.conf.urls import patterns, include, url
from races import views as races_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'athlet_stats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^races/', races_views.RaceList.as_view(), name="racelist"),
    url(r'^new/race/', races_views.NewRace.as_view(), name="newrace"),
    url(r'^new/edition/(?P<pk>[0-9]+)/$', races_views.NewEdition.as_view(), name="newedition"),
    url(r'^race/(?P<pk>[0-9]+)/$', races_views.EditionList.as_view(), name="editionlist"),
    url(r'^edition/(?P<pk>[0-9]+)/$', races_views.EditionDetail.as_view(), name="editiondetail"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weblog/', include('zinnia.urls')),
	url(r'^comments/', include('django.contrib.comments.urls')),
)