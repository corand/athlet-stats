from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.http import Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.http import HttpResponse,HttpResponseRedirect


class Blog(LoginRequiredMixin,TemplateView):
	template_name = "blog/blog.html"
	def get_context_data(self, **kwargs):
		context = super(Blog, self).get_context_data(**kwargs)
		context['borradores'] = Post.objects.filter(status=1,author=self.request.user)
		context['publicos'] = Post.objects.filter(status=2,author=self.request.user)
		context['privados'] = Post.objects.filter(status=3,author=self.request.user)
		return context


class NewPost(LoginRequiredMixin,CreateView):
	form_class = PostForm
	template_name = "blog/new_post.html"
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.author = self.request.user
		return super(NewPost, self).form_valid(form)
	def get_success_url(self):
		return reverse("blog")


class UpdatePost(LoginRequiredMixin,UpdateView):
	form_class = PostForm
	template_name = "blog/update_post.html"
	def get_success_url(self):
		return reverse("blog")
    
	def get_object(self, queryset=None):
		obj = Post.objects.get(id=self.kwargs['pk'])
		if not obj.author == self.request.user:
			raise Http404
		return obj

class DeletePost(LoginRequiredMixin,DeleteView):
	form_class = PostForm
	template_name = "blog/delete_post.html"
	def get_success_url(self):
		return reverse("blog")
	def get_object(self, queryset=None):
		obj = Post.objects.get(id=self.kwargs['pk'])
		if not obj.author == self.request.user:
			raise Http404
		return obj
	def get_context_data(self, **kwargs):
		context = super(DeletePost, self).get_context_data(**kwargs)
		context['post'] = Post.objects.get(id=self.kwargs['pk'])
		return context