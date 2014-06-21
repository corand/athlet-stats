from django.shortcuts import render
from .models import Race,Edition,Result
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from braces.views import LoginRequiredMixin
from django.shortcuts import render_to_response,get_object_or_404
# Create your views here.


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
		context['results'] = Result.objects.filter(edition__race=self.kwargs['pk']).order_by('position','edition__date')
		return context