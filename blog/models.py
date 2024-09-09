from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.conf import settings
import math

class Image(models.Model):
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    alt = models.CharField(max_length=255, default='Image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caption}"
        
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    post_url = models.CharField(max_length=255, unique=True, blank=True)
    featured_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='featured_blog_posts')
    content = RichTextField(config_name='awesome_ckeditor')
    content_snippet = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    def save(self, *args, **kwargs):
        if not self.post_url or self.title != BlogPost.objects.get(pk=self.pk).title:
            self.post_url = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def reading_time(self):
        words = len(self.content.split())
        reading_time_minutes = math.floor(words/200)
        return reading_time_minutes
    
    class Meta:
        ordering = ['-id']