from django.db import models
from datetime import datetime

# Create your models here.


class contactus(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    message=models.TextField()
    date_time=models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.name+' '+self.email+' '+self.message
