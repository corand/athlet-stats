from django.conf.urls import patterns, include, url
from races import views as races_views
from blog import views as blog_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'athlet_stats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^competiciones/', races_views.RaceList.as_view(), name="racelist"),
    url(r'^nueva/competicion/', races_views.NewRace.as_view(), name="newrace"),
    url(r'^nueva/edicion/(?P<id_race>[0-9]+)/$', races_views.NewEdition, name="newedition"),
    url(r'^nueva/edicion/prueba/(?P<id_subrace>[0-9]+)/$', races_views.NewEditionSubRace, name="neweditionsubrace"),
    url(r'^nueva/prueba/(?P<id_race>[0-9]+)/$', races_views.NewSubRace.as_view(), name="newsubrace"),
    url(r'^nuevo/resultado/(?P<id_edition>[0-9]+)/$', races_views.NewResult, name="newresult"),
    url(r'^competicion/(?P<pk>[0-9]+)/$', races_views.EditionList.as_view(), name="editionlist"),
    url(r'^edicion/(?P<pk>[0-9]+)/$', races_views.EditionDetail.as_view(), name="editiondetail"),
    url(r'^prueba/(?P<pk>[0-9]+)/$', races_views.SubRaceDetail.as_view(), name="subracedetail"),
    url(r'^changemodality/', races_views.changeModality, name="changemodality"),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^comments/', include('django.contrib.comments.urls')),
	url(r'^cerrar/$', races_views.cerrar),
	url(r'^login/$', races_views.login, name="login"),
    url(r'^nuevo/post/$', blog_views.NewPost.as_view(),name="newblogpost"),
    url(r'^editar/post/(?P<pk>[0-9]+)/$', blog_views.UpdatePost.as_view(),name="updateblogpost"),
    url(r'^eliminar/post/(?P<pk>[0-9]+)/$', blog_views.DeletePost.as_view(),name="deleteblogpost"),
    url(r'^blog/$', blog_views.Blog.as_view(),name="blog"),
    url(r'^ckeditor/', include('ckeditor.urls')),
)