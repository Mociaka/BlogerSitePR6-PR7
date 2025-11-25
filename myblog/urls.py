from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Подключаем urls приложения blog

]
