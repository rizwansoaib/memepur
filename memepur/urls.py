"""memepur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


from home import views as h

from login import views as l

from notifications import views as n



from django.contrib.sitemaps.views import sitemap

from home.sitemaps import *

sitemaps = {
        "posts": PhotoSitemap,
}


urlpatterns = [
    path('', h.index, name='home'),
    path('trending', h.trending,name='trending'),
    path('recent', h.recent,name='recent'),







    path('tag/<slug:tag_slug>', h.tag, name='tag'),
    path('admin/', admin.site.urls),
    path('login/', l.login,name='login'),
    path('profile/', l.profile),
    path('accounts/', include('allauth.urls')),

    path('upload/', h.upload),

    path('auto', h.autocomplete, name='autocomplete'),
    path('likepost', h.likepost, name='likepost'),
    path('delpost', h.delete_post, name='delpost'),
    path('likecomment', h.likecomment, name='likecomment'),
    path('post', h.post, name='post'),
    path('delcomment', h.delete_comment, name='delcomment'),



    path('followurl',l.followurl,name='followurl'),
    path('pro_likes',l.pro_liked,name='pro_likes'),
    path('followers',l.follower_list,name='followers'),
    path('following',l.following_list,name='following'),
    path('memes', l.pro_post, name='memes'),
    path('privacy', l.privacy, name='privacy'),
    path('contact', l.contact, name='contact'),





    path('notifications', n.notifications, name='notifications'),
    path('noti_count', n.noti_count, name='noti_count'),




path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                        name='django.contrib.sitemaps.views.sitemap'),

path('robots.txt',h.robots,name='robots.txt'),



]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'login.views.error404'

