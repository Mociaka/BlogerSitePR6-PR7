from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator
from taggit.managers import TaggableManager


class Post(models.Model):
    class PublishedManager(models.Manager):
     def get_queryset(self):

        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()  # менеджер за замовчуванням
    published = PublishedManager()  #
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def post_list(request):
        post_list = Post.published.all()
        # Пагінація з 3 постами на сторінку
        paginator = Paginator(post_list, 3)
        page_number = request.GET.get('page', 1)
        posts = paginator.page(page_number)

        return render(request, 'blog/post/list.html', {'posts': posts})

    tags = TaggableManager()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'







