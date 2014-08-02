from django.shortcuts import render
from braces.views import LoginRequiredMixin
from .forms import PostForm
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView

# Create your views here.
class NewPost(LoginRequiredMixin,CreateView):
	form_class = PostForm
	template_name = "blog/new_post.html"