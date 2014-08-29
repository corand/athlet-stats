from django.shortcuts import render
from blog.models import Post
from django.views.generic import TemplateView,ListView,DetailView




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