from django.shortcuts import render
from braces.views import LoginRequiredMixin
from .forms import PostForm
from .models import Post,PostEs,PostEus
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.http import HttpResponse,HttpResponseRedirect


def NewPost(request):
	if request.method=='POST':
		form = PostForm(request.POST)
		if form.is_valid():
			title_es = form.cleaned_data['title_es']
			title_eu = form.cleaned_data['title_eu']
			body_es = form.cleaned_data['body_es']
			body_eu = form.cleaned_data['body_eu']
			status = form.cleaned_data['status']
			new_post = Post(author=request.user,status=status)
			new_post.save()
			post_es = PostEs(title=title_es,body=body_es,post=new_post)
			post_es.save()
			post_eus = PostEus(title=title_eu,body=body_eu,post=new_post)
			post_eus.save()
			return HttpResponseRedirect(reverse("racelist"))
	else:
		form = PostForm()
	return render_to_response('blog/new_post.html',{'form':form},context_instance=RequestContext(request))