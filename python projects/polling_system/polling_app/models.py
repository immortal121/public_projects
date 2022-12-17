from django.db import models
from django.contrib.auth.models import User



# Create your models here.


class Questions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField(max_length=150)
    option1 = models.CharField(max_length=100,default=0)
    option2 = models.CharField(max_length=100,default=0)
    option3 = models.CharField(max_length=100,default=0)
    option4 = models.CharField(max_length=100,default=0)
    option1_count = models.IntegerField(default=0)
    option2_count = models.IntegerField(default=0)
    option3_count = models.IntegerField(default=0)
    option4_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    visited = models.BooleanField(default=False)

class phone_no(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ques_can_add = models.PositiveSmallIntegerField(default=5)
    phoneno = models.CharField(max_length=13,blank=True)

# delete questions which are created  24 hours before


