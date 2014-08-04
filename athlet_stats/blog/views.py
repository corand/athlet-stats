from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
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



@login_required(login_url="/login")
def NewPost(request):
	if request.method=='POST':
		form = PostForm(request.POST)
		if form.is_valid():
			title_es = form.cleaned_data['title_es']
			title_eu = form.cleaned_data['title_eu']
			body_es = form.cleaned_data['body_es']
			body_eu = form.cleaned_data['body_eu']
			status = form.cleaned_data['status']
			new_post = Post(title_es=title_es,body_es=body_es,title_eu=title_eu,body_eu=body_eu,author=request.user,status=status)
			new_post.save()
			return HttpResponseRedirect(reverse("racelist"))
	else:
		form = PostForm()
	return render_to_response('blog/new_post.html',{'form':form},context_instance=RequestContext(request))