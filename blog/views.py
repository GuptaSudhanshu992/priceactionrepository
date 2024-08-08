from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import BlogPost
from django.contrib import messages

class BlogView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.all()
    template_name = 'blog/blog.html'
    paginate_by = 10

class DetailArticleView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post.html'
    #context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        post_url = self.kwargs.get('post_url')
        return get_object_or_404(BlogPost, post_url=post_url)
    
    '''def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        context['liked_by_user'] = False
        blogpost = BlogPost.objects.get(id=self.kwargs.get('pk'))
        if blogpost.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        return context'''

def custom_404(request, exception):
    messages.warning(request, "ERROR 404: The URL that you are trying to access does not exist.")
    return redirect('/blog/')