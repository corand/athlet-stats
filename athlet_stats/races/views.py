from django.shortcuts import render
from .models import Race,Edition,Result
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from braces.views import LoginRequiredMixin
from django.shortcuts import render_to_response,get_object_or_404
# Create your views here.


class RaceList(LoginRequiredMixin,ListView):
	template_name = "races/race_list.html"
	paginate_by = 150
	context_object_name = 'races'
	def get_queryset(self):
		return Race.objects.all().order_by('month','week')

class EditionList(LoginRequiredMixin,ListView):
	template_name = "races/edition_list.html"
	paginate_by = 150
	context_object_name = 'editions'
	def get_queryset(self):
		return Edition.objects.filter(race=self.kwargs['pk']).order_by('date')

	def get_context_data(self, **kwargs):
		context = super(EditionList, self).get_context_data(**kwargs)
		context['race'] = get_object_or_404(Race,pk=self.kwargs['pk'])
		context['results'] = Result.objects.filter(edition__race=self.kwargs['pk']).order_by('position','edition__date')
		return context