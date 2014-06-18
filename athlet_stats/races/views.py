from django.shortcuts import render
from .models import Race
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from braces.views import LoginRequiredMixin
# Create your views here.


class RaceList(LoginRequiredMixin,ListView):
	template_name = "races/race_list.html"
	paginate_by = 150
	context_object_name = 'races'
	def get_queryset(self):
		return Race.objects.all().order_by('month','week')