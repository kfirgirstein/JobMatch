"""
Definition of models.
"""

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import datetime

#python manage.py makemigrations --name inital app
#python manage.py migrate


class Company(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    threshold = models.PositiveIntegerField(validators=[MaxValueValidator(10),MinValueValidator(99)],default=55)
    num_of_questions = models.PositiveIntegerField(validators=[MaxValueValidator(1),MinValueValidator(10)],default=10)
    num_of_clusters = models.PositiveIntegerField(validators=[MaxValueValidator(1),MinValueValidator(10)],default=1)

class Question(models.Model):
    description = models.CharField(max_length=256)
    option_a = models.CharField(max_length=256,default="Yes")
    option_b = models.CharField(max_length=256,default="No")
    option_c = models.CharField(max_length=256,blank=True,null=True,default=None)
    option_d = models.CharField(max_length=256,blank=True,null=True,default=None)
    correct_answer = models.PositiveSmallIntegerField(validators=[MaxValueValidator(1),MinValueValidator(4)],default=1)
    
# 1 - not checked yet, 2 - passed, 3 - failed he interview, 4 - failed the quistinaire
class Status(models.Model):
    description = models.CharField(max_length=256)

class Clusters(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

class Questions_weights(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    cluster = models.ForeignKey(Clusters,on_delete=models.CASCADE)
    weight = models.FloatField(default=10.0)
    class Meta:
        unique_together = (('question', 'cluster'),)


class Submissions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    answeres = models.CharField(max_length=256)
    class Meta:
        unique_together = (('user', 'company'),)



    
# Create your models here.
