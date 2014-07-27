from django.shortcuts import render
from .models import Race,Edition,Result,Modality,SubRace
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.template import RequestContext
from .forms import RaceForm,EditionForm,SubRaceForm
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from braces.views import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/sarrera')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario,password=clave)
            if acceso is not None:
                authForm(request,acceso)
                return HttpResponseRedirect('/competiciones/')
            else:
                return render_to_response('ezaktibo.html',context_instance=RequestContext(request))
        else:
            return render_to_response('ezaktibo.html',context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
        formulario.fields['username'].widget.attrs['class'] = "form-control"
    	formulario.fields['password'].widget.attrs['class'] = "form-control"
    	formulario.fields['username'].widget.attrs['placeholder'] = "Nombre de Usuario"
    	formulario.fields['password'].widget.attrs['placeholder'] = "Password"
    return render_to_response('races/login.html',{'formulario':formulario},context_instance=RequestContext(request))




class RaceList(LoginRequiredMixin,TemplateView):
	template_name = "races/race_list.html"
	paginate_by = 150
	context_object_name = 'races'
	def get_context_data(self, **kwargs):
		context = super(RaceList, self).get_context_data(**kwargs)
		context['septiembre'] = Race.objects.filter(month=9).order_by('week','name')
		context['octubre'] = Race.objects.filter(month=10).order_by('week','name')
		context['noviembre'] = Race.objects.filter(month=11).order_by('week','name')
		context['diciembre'] = Race.objects.filter(month=12).order_by('week','name')
		context['enero'] = Race.objects.filter(month=1).order_by('week','name')
		context['febrero'] = Race.objects.filter(month=2).order_by('week','name')
		context['marzo'] = Race.objects.filter(month=3).order_by('week','name')
		context['abril'] = Race.objects.filter(month=4).order_by('week','name')
		context['mayo'] = Race.objects.filter(month=5).order_by('week','name')
		context['junio'] = Race.objects.filter(month=6).order_by('week','name')
		context['julio'] = Race.objects.filter(month=7).order_by('week','name')
		context['agosto'] = Race.objects.filter(month=8).order_by('week','name')
		return context

class EditionList(LoginRequiredMixin,ListView):
    template_name = "races/edition_list.html"
    paginate_by = 150
    context_object_name = 'editions'
    def get_queryset(self):
        return Edition.objects.filter(race=self.kwargs['pk']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(EditionList, self).get_context_data(**kwargs)
        context['race'] = get_object_or_404(Race,pk=self.kwargs['pk'])
        context['subraces'] = SubRace.objects.filter(race=self.kwargs['pk']).order_by('name')
        context['results'] = Result.objects.filter(edition__race=self.kwargs['pk']).order_by('position','-edition__date')
        return context

class EditionDetail(LoginRequiredMixin,ListView):
	template_name = "races/edition_detail.html"
	context_object_name = 'results'
	def get_queryset(self):
		return Result.objects.filter(edition=self.kwargs['pk']).order_by('position')
	def get_context_data(self, **kwargs):
		context = super(EditionDetail, self).get_context_data(**kwargs)
		context['edition'] = get_object_or_404(Edition,pk=self.kwargs['pk'])
		return context

class NewRace(LoginRequiredMixin,CreateView):
    form_class = RaceForm
    template_name = "races/new_race.html"
    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        return super(NewRace,self).form_valid(form)

    def get_success_url(self):
        return reverse("racelist")

class NewSubRace(LoginRequiredMixin,CreateView):
    form_class = SubRaceForm
    model = SubRace
    template_name = "races/subrace_form.html"

    def dispatch(self, *args, **kwargs):
        self.race = get_object_or_404(Race, pk=self.kwargs['id_race'])
        return super(NewSubRace, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        form = super(NewSubRace, self).get_form(form_class)
        form.instance.race = self.race
        return form
    def get_context_data(self, **kwargs):
        context = super(NewSubRace, self).get_context_data(**kwargs)
        context['race'] = self.race
        return context

    def get_success_url(self):
        return reverse("racelist")

@login_required(login_url='races/login')
def NewEdition(request,id_race):
    race = get_object_or_404(Race, pk=id_race)
    if request.method=='POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            edition_type = get_object_or_404(Modality,id=form.cleaned_data['modality'])
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            new_edition = Edition(type=edition_type,date=date,race=race,name=name,creator=request.user)
            new_edition.save()
            return HttpResponseRedirect(reverse("racelist"))
    else:
        form = EditionForm()

    return render_to_response('races/new_edition.html',{'form':form,'race':race},context_instance=RequestContext(request))


@login_required(login_url='races/login')
def changeModality(request):
    objectQuerySet = Modality.objects.filter(race_type=request.POST['race_type']).order_by('modality')
    data = serializers.serialize('json', objectQuerySet, fields=('id','modality'))

    return HttpResponse(data,content_type='application/json')


@login_required(login_url='races/login')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/login')
