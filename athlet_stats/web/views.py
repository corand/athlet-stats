from django.shortcuts import render
from blog.models import Post
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import translation
from races.models import Edition,Result
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from django.utils.timezone import utc
import json
import dateutil.parser
from django.conf import settings
from django.core.cache import cache
from django.conf import settings
import flickr_api


class PostList(ListView):
    template_name = "web/blog.html"
    paginate_by = 3
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(status=2).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context["active"] = "blog"
        enddate = datetime.now().date() + timedelta(days=1)
        startdate = enddate - timedelta(days=30)
        context['results'] = Result.objects.filter(edition__date__range=[startdate,enddate]).order_by('-edition__date','edition__name','user__gender','position','timemark')
        return context



class Calendar(TemplateView):
    template_name = "web/calendar.html"
    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)
        context["active"] = "calendar"
        enddate = datetime.now().date() + timedelta(days=1)
        startdate = enddate - timedelta(days=30)
        context['results'] = Result.objects.filter(edition__date__range=[startdate,enddate]).order_by('-edition__date','edition__name','user__gender','position','timemark')
        return context


class Results(TemplateView):
    template_name = "web/results.html"
    def get_context_data(self,**kwargs):
        context = super(Results, self).get_context_data(**kwargs)
        context["active"] = "results"
        enddate = datetime.now().date() + timedelta(days=1)
        startdate = datetime(2014,9,1)
        context["results"] = Result.objects.filter(edition__date__range=[startdate,enddate]).order_by('-edition__date', 'edition__race','edition__name','user__gender','position','timemark')
        return context

class Albums(TemplateView):
    template_name = "web/albums.html"
    def get_context_data(self,**kwargs):
        context = super(Albums, self).get_context_data(**kwargs)
        flickr_api.enable_cache(cache)
        flickr_api.set_keys(api_key=settings.FLICKR_API,api_secret=settings.FLICKR_SECRET)
        user = flickr_api.Person.findByUserName('aloinargixao')
        photosets = user.getPhotosets()

        albums = []
        for photoset in photosets:
            pic = photoset.getPhotos()[:1]
            thumb_source = pic[0].getSizes()['Small']['source']
            dict = {'id':photoset.id,'title':photoset.title,'pic':thumb_source}
            albums.append(dict)

        context['albums'] = albums
        context["active"] = "album"
        return context

class Album(TemplateView):
    template_name = "web/album.html"
    def get_context_data(self,**kwargs):
        context = super(Album, self).get_context_data(**kwargs)
        flickr_api.enable_cache(cache)
        
        flickr_api.set_keys(api_key=settings.FLICKR_API,api_secret=settings.FLICKR_SECRET)
        user = flickr_api.Person.findByUserName('aloinargixao')
        photosets = user.getPhotosets()

        for photoset in photosets:
            if photoset.id == self.kwargs['pk']:
                my_photoset = photoset
                my_title = photoset.title

        pictures = my_photoset.getPhotos()
        picture_list = []
        for picture in pictures:
            dict = {'medium':picture.getSizes()['Medium']['source'],'large':picture.getSizes()['Large']['source']}
            picture_list.append(dict)

        context['picture_list'] = picture_list
        context['title'] = my_title
        context['id'] = self.kwargs['pk']
        context["active"] = "album"
        return context



class Archive(ListView):
    template_name = "web/archive.html"
    paginate_by = 100
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(status=2).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(Archive, self).get_context_data(**kwargs)
        context["active"] = "archive"
        return context



class AboutUs(TemplateView):
    template_name = "web/about_us.html"
    def get_context_data(self, **kwargs):
        context = super(AboutUs, self).get_context_data(**kwargs)
        context["active"] = "about"
        return context


class PostView(DetailView):
    model = Post
    template_name = "web/post.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        lang = request.LANGUAGE_CODE
        user_language = lang

        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language

        if lang == 'es':
            if post.slug_es != self.kwargs['slug']:
                return HttpResponseRedirect(reverse('post', kwargs={'pk':post.id,'slug':post.slug_es}))
        else:
            if post.slug_eu != self.kwargs['slug']:
                return HttpResponseRedirect(reverse('post', kwargs={'pk':post.id,'slug':post.slug_eu}))

        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        soup_eu = BeautifulSoup(post.body_eu)
        soup_es = BeautifulSoup(post.body_es)
        img_eu = soup_eu.find('img')
        img_es = soup_es.find('img')
        if img_eu:
            context['imagen_eu'] = img_eu['src']
        if img_es:
            context['imagen_es'] = img_es['src']
        return context
    

def eventsFeed(request):
    json_list = []
    if request.is_ajax():
        print 'Its ajax from fullCalendar()'
        #print request.GET.get('start','False')

        start = dateutil.parser.parse(request.GET.get('start'))
        end = dateutil.parser.parse(request.GET.get('end'))
        print start
        print end

        races = Edition.objects.filter(date__gte=start).filter(date__lte=end)

        for race in races:
            id = race.id
            title = race.name
            settingstime_zone = timezone(settings.TIME_ZONE)
            start = race.date.astimezone(settingstime_zone)
            #start = race.date.strftime("%Y-%m-%dT%H:%M:%S")
            print start
            allDay = False

            json_entry = {'id':id, 'start':str(start), 'allDay':allDay, 'title': title}
            json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')