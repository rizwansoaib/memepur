from django.contrib.sitemaps import Sitemap

from home.models import *

class PhotoSitemap(Sitemap):
        changefreq = "daily"
        priority = 0.9

        def items(self):
                return photo.objects.all()

        def lastmod(self, obj):
                return obj.date_time

        def image(self,obj):
                return obj.url

        def title(self,obj):
                return obj.title

        def tags(self,obj):
                return obj.tags.all