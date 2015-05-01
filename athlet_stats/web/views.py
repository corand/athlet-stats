from django.shortcuts import render
from blog.models import Post
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import translation
from races.models import Edition,Result,Race,Season,Modality
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
from django.db import connection


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
        startdate = enddate - timedelta(days=15)
        context['results'] = Result.objects.filter(edition__date__range=[startdate,enddate]).order_by('-edition__date','edition__name','user__gender','position','timemark')
        return context



class Calendar(TemplateView):
    template_name = "web/calendar.html"
    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)
        context["active"] = "calendar"
        enddate = datetime.now().date() + timedelta(days=1)
        startdate = enddate - timedelta(days=15)
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
        album_id = self.kwargs['pk']
        my_title = "xx"
        
        
        try:
            json_data = open("/opt/django_cache/json/"+album_id+".json")
            result = json.load(json_data)
            picture_list = result['photoset']
            my_title= result['title']
        except IOError: 
            flickr_api.set_keys(api_key=settings.FLICKR_API,api_secret=settings.FLICKR_SECRET)
            user = flickr_api.Person.findByUserName('aloinargixao')
            photosets = user.getPhotosets()

            for photoset in photosets:
                if photoset.id == album_id:
                    my_photoset = photoset
                    my_title = photoset.title

            pictures = my_photoset.getPhotos()
            picture_list = []
            for picture in pictures:
                dict = {'medium':picture.getSizes()['Medium']['source'],'large':picture.getSizes()['Large']['source']}
                picture_list.append(dict)

            result = {'title':my_title,'photoset':picture_list}

            #cache.set(album_id,picture_list,0)
            with open("/opt/django_cache/json/"+album_id+".json", "w+") as out:
                data = json.dumps(result)
                out.write(data)

        context['picture_list'] = picture_list
        context['title'] = my_title
        context['id'] = album_id
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
        else:
            if img_es:
                context['imagen_eu'] = img_es['src']
        if img_es:
            context['imagen_es'] = img_es['src']
        else:
            if img_eu:
                context['imagen_es'] = img_eu['src']

        enddate = datetime.now().date() + timedelta(days=1)
        startdate = enddate - timedelta(days=15)
        context['results'] = Result.objects.filter(edition__date__range=[startdate,enddate]).order_by('-edition__date','edition__name','user__gender','position','timemark')
        return context

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

class SeasonRanking(TemplateView):
    template_name = "web/season_ranking.html"
    def get_context_data(self, **kwargs):
        context = super(SeasonRanking, self).get_context_data(**kwargs)
        season = get_object_or_404(Season,name=self.kwargs['slug'])
        cursor = connection.cursor()

        #pista aire libre masculino
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 4 AND pu.gender = 1 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"' AND pu2.gender=pu.gender) order by rm.distance");
        context["aire_libre_masculino"] = dictfetchall(cursor)

        #lanzamientos
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,distancemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 4 AND pu.gender = 1 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'distance' AND rr.distancemark = ( Select max(rr2.distancemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance")
        context["aire_libre_lanzamientos_masculino"] = dictfetchall(cursor)


        #pista aire libre femenino
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 4 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"'  AND pu.gender = 2 AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance");
        context["aire_libre_femenino"] = dictfetchall(cursor)

        #lanzamientos
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,distancemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 4 AND pu.gender = 2 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'distance' AND rr.distancemark = ( Select max(rr2.distancemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance")
        context["aire_libre_lanzamientos_femenino"] = dictfetchall(cursor)

        # pista cubierta masculino
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 3 AND pu.gender = 1 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"' AND pu2.gender=pu.gender) order by rm.distance");
        context["cubierta_masculino"] = dictfetchall(cursor)
        # lanzamientos
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,distancemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 3 AND pu.gender = 1 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'distance' AND rr.distancemark = ( Select max(rr2.distancemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance")
        context["cubierta_lanzamientos_masculino"] = dictfetchall(cursor)

        # pista cubierta femenino
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 3 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"'  AND pu.gender = 2 AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance");
        context["cubierta_femenino"] = dictfetchall(cursor)
        # lanzamientos
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,distancemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 3 AND pu.gender = 2 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rrt.name = 'distance' AND rr.distancemark = ( Select max(rr2.distancemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"'  AND pu2.gender=pu.gender) order by rm.distance")
        context["cubierta_lanzamientos_femenino"] = dictfetchall(cursor)

        # asfalto
        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 1 AND pu.gender = 1 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"'  AND modality != 'Otro' AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"' AND pu2.gender=pu.gender) order by rm.distance")
        context["asfalto_masculino"] = dictfetchall(cursor)

        cursor.execute("Select distinct rm.id AS modality_id,modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id Where rm.race_type_id = 1 AND pu.gender =2 AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"'  AND modality != 'Otro' AND rrt.name = 'duration' AND rr.timemark = ( Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where rm2.id=rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"' AND pu2.gender=pu.gender) order by rm.distance")
        context["asfalto_femenino"] = dictfetchall(cursor)

        context["season"] = season
        context["active"] = "ranking"

        return context

class ModalitySeasonRanking(TemplateView):
    template_name = "web/modality_season_ranking.html"
    def get_context_data(self, **kwargs):
        context = super(ModalitySeasonRanking, self).get_context_data(**kwargs)
        season = get_object_or_404(Season,pk=self.kwargs['season_id'])
        modality = get_object_or_404(Modality,pk=self.kwargs['mod_id'])
        
        if self.kwargs['gender'] == 'masc':
            gender = 1
        else:
            gender = 2

        dist_time = self.kwargs['dist_time']
        cursor = connection.cursor()

        if(dist_time == 'time'):
            cursor.execute("Select distinct rm.id, modality, rm.distance,timemark, pu.name AS izena, pu.first_surname,pu.second_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id WHERE pu.gender = "+str(gender)+" AND rm.id = "+str(modality.id)+" AND rr.timemark = (Select min(rr2.timemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where pu.id=pu2.id AND rm2.id = rm.id) order by timemark")
        else:
            cursor.execute("Select distinct rm.id, modality, rm.distance,distancemark, pu.name AS izena, pu.first_surname,pu.second_surname,re.name,re.date From races_result as rr Inner Join races_edition as re on rr.edition_id = re.id Inner Join races_modality as rm on re.type_id = rm.id Inner Join profiles_userprofile as pu on rr.user_id = pu.id Inner Join races_resulttype as rrt on rm.result_type_id = rrt.id WHERE pu.gender = "+str(gender)+" AND re.date > '"+ str(season.start_date) +"' AND re.date < '"+ str(season.end_date) +"' AND rm.id = "+str(modality.id)+" AND rr.distancemark = (Select max(rr2.distancemark) From races_result as rr2 Inner Join races_edition as re2 on rr2.edition_id = re2.id Inner Join races_modality as rm2 on re2.type_id = rm.id Inner Join profiles_userprofile as pu2 on rr2.user_id = pu2.id Where pu.id=pu2.id AND rm2.id = rm.id AND re2.date > '"+ str(season.start_date) +"' AND re2.date < '"+ str(season.end_date) +"') order by distancemark desc")
        
        context["ranking"] = dictfetchall(cursor)
        context["season"] = season
        context["modality"] = modality
        context["active"] = "ranking"

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

        # Race.objects.filter(edition__name__contains='a')
        races = Race.objects.filter(edition__date__gte=start).filter(edition__date__lte=end).distinct('id')

        for race in races:
            id = race.id
            title = race.name
            settingstime_zone = timezone(settings.TIME_ZONE)
            start = race.edition_set.select_related()[0].date.astimezone(settingstime_zone)
            #start = race.date.strftime("%Y-%m-%dT%H:%M:%S")
            allDay = False

            json_entry = {'id':id, 'start':str(start), 'allDay':allDay, 'title': title}
            json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')