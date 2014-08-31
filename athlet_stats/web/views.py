from django.shortcuts import render
from blog.models import Post
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from bs4 import BeautifulSoup




class PostList(ListView):
    template_name = "web/blog.html"
    paginate_by = 3
    context_object_name = 'posts'
    def get_queryset(self):
        return Post.objects.filter(status=2).order_by('-created')


class PostView(DetailView):
    model = Post
    template_name = "web/post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        soup_eu = BeautifulSoup(post.body_eu)
        soup_es = BeautifulSoup(post.body_es)
        context['imagen_eu'] = soup_eu.find('img')['src']
        context['imagen_es'] = soup_es.find('img')['src']
        return context