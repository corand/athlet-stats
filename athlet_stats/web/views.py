from django.shortcuts import render
from blog.models import Post
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import translation



class PostList(ListView):
    template_name = "web/blog.html"
    paginate_by = 3
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(status=2).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context["active"] = "blog"
        return context


class Archive(ListView):
    template_name = "web/archive.html"
    paginate_by = 100
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(status=2).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(Archive, self).get_context_data(**kwargs)
        context["active"] = "archive"
        return context



class AboutUs(TemplateView):
    template_name = "web/about_us.html"
    def get_context_data(self, **kwargs):
        context = super(AboutUs, self).get_context_data(**kwargs)
        context["active"] = "about"
        return context


class PostView(DetailView):
    model = Post
    template_name = "web/post.html"
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        lang = request.LANGUAGE_CODE
        user_language = lang

        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language

        if lang == 'es':
            if post.slug_es != self.kwargs['slug']:
                return HttpResponseRedirect(reverse('post', kwargs={'pk':post.id,'slug':post.slug_es}))
        else:
            if post.slug_eu != self.kwargs['slug']:
                return HttpResponseRedirect(reverse('post', kwargs={'pk':post.id,'slug':post.slug_eu}))

        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        soup_eu = BeautifulSoup(post.body_eu)
        soup_es = BeautifulSoup(post.body_es)
        img_eu = soup_eu.find('img')
        img_es = soup_es.find('img')
        if img_eu:
            context['imagen_eu'] = img_eu['src']
        if img_es:
            context['imagen_es'] = img_es['src']
        return context
    