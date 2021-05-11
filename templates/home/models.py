import uuid
from datetime import datetime

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User



from django.conf import settings
# Create your models here.



def my_uuid():
    return 'a'+str(uuid.uuid4())[:-1]

class photo(models.Model):
    photo_id=models.CharField(max_length=16, unique=True, default=my_uuid)
    title=models.TextField()
    url=models.ImageField(upload_to='uploads/')
    uploader=models.ForeignKey(User,on_delete=models.CASCADE)
    view_count = models.BigIntegerField(default=0)
    date_time=models.DateTimeField(default=datetime.now)
    tags=TaggableManager()


    def __str__(self):
        return str(self.photo_id) if self.photo_id else ''

    def count_likes(self):
        return user_likes_photo.objects.filter(photo_id=self).count()
    def count_comments(self):
        return user_comments.objects.filter(photo_id=self).count()
    def count_views(self):
        return self['view_count']

    def get_absolute_url(self):
        return "/post?id=%s" % self.photo_id





class user_likes_photo(models.Model):
    photo_id = models.ForeignKey(photo, on_delete=models.CASCADE)
    username= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def get_post(self):
        return photo.objects.filter(photo_id=self)

    def __str__(self):
        return str(self.photo_id) if self.photo_id else ''



class user_comments(models.Model):
    comment_id=models.CharField(max_length=16, unique=True, default=my_uuid)
    photo_id = models.ForeignKey(photo, on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    data= models.TextField()
    date_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.comment_id) if self.comment_id else ''
    def count_comment_likes(self):
        return user_likes_comment.objects.filter(comment_id=self).count()




class user_likes_comment(models.Model):
    comment_id = models.ForeignKey(user_comments, on_delete=models.CASCADE)
    username= models.ForeignKey(
        settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.comment_id) if self.comment_id else ''




class follow(models.Model):
    username = models.CharField(max_length=100)
    follow = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)

    def get_follower_count(self):
        return follow.objects.filter(username=self.username).count()

    def get_following_count(self):
        return follow.objects.filter(follow=self).count()

    def get_follower_list(self):
        return follow.objects.filter(username=self.username)

    def get_following_list(self):
        return follow.objects.filter(follow=self)




class recommender(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    tag=models.CharField(max_length=32,primary_key=True)
    view_count=models.BigIntegerField(default=0)
    like_count=models.BigIntegerField(default=0)
    comment_count=models.BigIntegerField(default=0)


    def get_recommender_score(self):
        self.view_count + self.like_count + 2 * self.comment_count

    def __str__(self):
        return str(self.username)+' '+self.tag+' '+str(self.view_count+self.like_count+2*self.comment_count)







