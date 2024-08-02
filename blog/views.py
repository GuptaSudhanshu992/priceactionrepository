from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost

class BlogView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.all().order_by('-date')
    template_name = 'blog/blog.html'
    paginate_by = 2

class DetailArticleView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post.html'
    
    '''def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        context['liked_by_user'] = False
        blogpost = BlogPost.objects.get(id=self.kwargs.get('pk'))
        if blogpost.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        return context'''