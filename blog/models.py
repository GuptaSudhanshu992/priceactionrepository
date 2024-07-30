from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    post_url = models.CharField(max_length=255, unique=True, blank=True)
    content = HTMLField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def save(self, *args, **kwargs):
        if not self.post_url or self.title != BlogPost.objects.get(pk=self.pk).title:
            self.post_url = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
