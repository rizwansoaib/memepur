from django.db import models

# Create your models here.


from django.contrib.auth.models import User
from datetime import datetime

notification_type=(
    ('1','following'),
    ('2','likememe'),
    ('3','commentmeme'),
    ('4','alsocomment'),
    ('5','likecomment'),

)


class user_notifications(models.Model):
    sender=models.CharField(max_length=32)
    receiver=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.CharField(choices=notification_type,max_length=32)
    message=models.TextField()
    url=models.URLField()
    read=models.BooleanField(default=False)
    date=models.DateTimeField(default=datetime.now)





    def __str__(self):
        return str(self.receiver.username+' '+self.message)





