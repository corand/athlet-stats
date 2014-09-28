from django.shortcuts import render
from .models import Race,Edition,Result,Modality,SubRace,RaceType,Objective
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.template import RequestContext
from .forms import RaceForm,EditionForm,SubRaceForm,ResultForm,ObjectiveForm
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from braces.views import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,timedelta
# Create your views here.

def login(request):
    if not request.user.is_anonymous():
        if request.user.is_authenticated():
            return HttpResponseRedirect('/private/blog/')
        else:
            return HttpResponseRedirect('/login')
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

class ObjectiveList(LoginRequiredMixin,ListView):
    template_name="races/objective_list.html"
    paginate_by = 150
    context_object_name = "objectives"
    def get_queryset(self):
        return Objective.objects.filter(user=self.request.user).order_by('-edition__date')


class ResultList(LoginRequiredMixin,ListView):
    template_name="races/result_list.html"
    paginate_by = 150
    context_object_name = "results"
    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).order_by('-edition__date')
 

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
        edition = get_object_or_404(Edition,pk=self.kwargs['pk'])
        if edition.distance:
            distance = edition.distance
        else:
            distance = edition.type.distance

        context['edition'] = edition
        context['distance'] = distance
        context['objectives'] = Objective.objects.filter(edition=self.kwargs['pk']).order_by('position')

        return context

class SubRaceDetail(LoginRequiredMixin,ListView):
    template_name = "races/subrace_detail.html"
    paginate_by = 150
    context_object_name = "editions"
    def get_queryset(self):
        return Edition.objects.filter(subRace=self.kwargs['pk']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(SubRaceDetail, self).get_context_data(**kwargs)
        context['subRace'] = get_object_or_404(SubRace,pk=self.kwargs['pk'])
        context['results'] = Result.objects.filter(edition__subRace=self.kwargs['pk']).order_by('position','-edition__date')
#        context['results'] = Result.objects.filter(edition__race=self.kwargs['pk']).order_by('position','-edition__date')
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
        return reverse("editionlist",kwargs={'pk':self.kwargs['id_race']})

@login_required(login_url="/login")
def NewEdition(request,id_race):
    race = get_object_or_404(Race, pk=id_race)
    if request.method=='POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            edition_type = get_object_or_404(Modality,id=form.cleaned_data['modality'])
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            distance = form.cleaned_data['distance']

            new_edition = Edition(type=edition_type,date=date,race=race,name=name,creator=request.user,distance=distance)
            new_edition.save()
            return HttpResponseRedirect(reverse("editionlist",kwargs={'pk':id_race}))
    else:
        form = EditionForm()

    return render_to_response('races/new_edition.html',{'form':form,'race':race},context_instance=RequestContext(request))



@login_required(login_url="/login")
def NewResult(request,id_edition):
    edition = get_object_or_404(Edition,pk=id_edition)
    if request.method=='POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['horas']:
                horas = form.cleaned_data['horas']
            else:
                horas = 0

            if form.cleaned_data['minutos']:
                minutos = form.cleaned_data['minutos']
            else:
                minutos = 0

            if form.cleaned_data['segundos']:
                segundos = form.cleaned_data['segundos']
            else:
                segundos = 0

            if form.cleaned_data['centesimas']:
                centesimas = form.cleaned_data['centesimas']
            else:
                centesimas = 0

            milisegundos = centesimas * 10
            timemark = timedelta(hours=horas,minutes=minutos,seconds=segundos,milliseconds=milisegundos)
            distancemark = form.cleaned_data['distancia']
            position = form.cleaned_data['puesto']
            comment = form.cleaned_data['comentarios']
            pos_cat = form.cleaned_data['puesto_cat']
            new_resultado = Result(user=request.user,edition=edition,timemark=timemark,distancemark=distancemark,position=position,position_cat=pos_cat,comment=comment)
            new_resultado.save()
            return HttpResponseRedirect(reverse("racelist"))
    else:
        form = ResultForm()

    return render_to_response("races/new_result.html",{'form':form,'edition':edition},context_instance=RequestContext(request))

@login_required(login_url="/login")
def NewObjective(request,id_edition):
    edition = get_object_or_404(Edition,pk=id_edition)
    if request.method=='POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['horas']:
                horas = form.cleaned_data['horas']
            else:
                horas = 0

            if form.cleaned_data['minutos']:
                minutos = form.cleaned_data['minutos']
            else:
                minutos = 0

            if form.cleaned_data['segundos']:
                segundos = form.cleaned_data['segundos']
            else:
                segundos = 0

            if form.cleaned_data['centesimas']:
                centesimas = form.cleaned_data['centesimas']
            else:
                centesimas = 0

            milisegundos = centesimas * 10
            timemark = timedelta(hours=horas,minutes=minutos,seconds=segundos,milliseconds=milisegundos)
            distancemark = form.cleaned_data['distancia']
            position = form.cleaned_data['puesto']
            comment = form.cleaned_data['comentarios']
            pos_cat = form.cleaned_data['puesto_cat']
            new_objetivo = Objective(user=request.user,edition=edition,timemark=timemark,distancemark=distancemark,position=position,position_cat=pos_cat,comment=comment)
            new_objetivo.save()
            return HttpResponseRedirect(reverse("racelist"))
    else:
        form = ObjectiveForm()

    return render_to_response("races/new_objective.html",{'form':form,'edition':edition},context_instance=RequestContext(request))


class DeleteObjective(LoginRequiredMixin,DeleteView):
    model = Objective
    template_name = "races/delete_objective.html"
    context_object_name = 'objective'
    
    def get_success_url(self):
        return reverse("objectives")
    
    def get_object(self, queryset=None):
        obj = Objective.objects.get(id=self.kwargs['pk'])
        if not obj.user == self.request.user:
            raise Http404
        return obj


@login_required(login_url="/login")
def editObjective(request, id_objective):
    objective = get_object_or_404(Objective, pk=id_objective)
    if request.method=='POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['horas']:
                horas = form.cleaned_data['horas']
            else:
                horas = 0

            if form.cleaned_data['minutos']:
                minutos = form.cleaned_data['minutos']
            else:
                minutos = 0

            if form.cleaned_data['segundos']:
                segundos = form.cleaned_data['segundos']
            else:
                segundos = 0

            if form.cleaned_data['centesimas']:
                centesimas = form.cleaned_data['centesimas']
            else:
                centesimas = 0

            milisegundos = centesimas * 10
            timemark = timedelta(hours=horas,minutes=minutos,seconds=segundos,milliseconds=milisegundos)
            distancemark = form.cleaned_data['distancia']
            position = form.cleaned_data['puesto']
            comment = form.cleaned_data['comentarios']
            pos_cat = form.cleaned_data['puesto_cat']
            objective.timemark = timemark
            objective.distancemark = distancemark
            objective.position = position
            objective.position_cat = pos_cat
            objective.comment = comment
            objective.save()
            return HttpResponseRedirect(reverse("objectives"))
    else:
        cent = 0
        hours = 0
        minutes = 0
        seconds = 0
        if objective.timemark:
            sec = str(objective.timemark.total_seconds()).split('.')[0]
            cent = str(objective.timemark.total_seconds()).split('.')[1]
            hours = int(sec) // 3600
            minutes = (int(sec) % 3600) // 60
            seconds = int(sec) % 60
        
        form = ObjectiveForm(initial={'horas': hours,'minutos':minutes,'segundos':seconds,'centesimas':cent,'distncia':objective.distancemark,'puesto':objective.position,'puesto_cat':objective.position_cat,'comentarios':objective.comment})
        return render_to_response('races/edit_objective.html', {'objective':objective,'form': form},context_instance=RequestContext(request)) 






@login_required(login_url="/login")
def NewEditionSubRace(request,id_subrace):
    subrace = get_object_or_404(SubRace, pk=id_subrace)
    race = get_object_or_404(Race,pk=subrace.race.id)
    if request.method=='POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            edition_type = get_object_or_404(Modality,id=form.cleaned_data['modality'])
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            new_edition = Edition(type=edition_type,date=date,race=race,name=name,subRace=subrace,creator=request.user)
            new_edition.save()
            return HttpResponseRedirect(reverse("racelist"))
    else:
        form = EditionForm()

    return render_to_response('races/new_subrace_edition.html',{'form':form,'subrace':subrace,'race':race},context_instance=RequestContext(request))


@login_required(login_url="/login")
def changeModality(request):
    objectQuerySet = Modality.objects.filter(race_type=request.POST['race_type']).order_by('order')
    data = serializers.serialize('json', objectQuerySet, fields=('id','modality'))

    return HttpResponse(data,content_type='application/json')


@login_required(login_url="/login")
def cerrar(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
