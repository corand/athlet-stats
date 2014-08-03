from django.shortcuts import render
from braces.views import LoginRequiredMixin
from .forms import PostForm
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView

# Create your views here.
class NewPost(LoginRequiredMixin,CreateView):
	form_class = PostForm
	template_name = "blog/new_post.html"



def NewPost(request):
	form = PostForm()
	return render_to_response('blog/new_post.html',{'form':form},context_instance=RequestContext(request))