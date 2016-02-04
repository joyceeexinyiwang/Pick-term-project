import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#infographics for casual choosing experience
class Goal(models.Model):
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.content

class Option(models.Model):
    #suggester = models.ForeignKey(Suggester)
    name = models.CharField(max_length=1000, default="")
    optionContent = models.CharField(max_length=1000)
    isResult = models.BooleanField(default=False)

    def __eq__(self, other):
        return self.optionContent == other.optionContent

    def __str__(self):
        return self.name

class Pro(models.Model):
    procontent = models.CharField(max_length=1000, default="")
    option = models.ForeignKey("Option", default="")

    def __str__(self):
        return self.procontent

    def __eq__(self, other):
        return self.procontent == other.procontent and self.option == other.option


class Con(models.Model):
    concontent = models.CharField(max_length=1000, default="")
    option = models.ForeignKey("Option", default="")

    def __str__(self):
        return self.concontent

    def __eq__(self, other):
        return self.concontent == other.concontent and self.option == other.option

class Criterion(models.Model):
    name = models.CharField(max_length=1000, default="")
    option = models.ForeignKey("Option", default="")
    weight = models.IntegerField(default=1) #1~5 scale

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

class Rate(models.Model):
    ratername = models.CharField(max_length=1000, default="")
    criterion = models.ForeignKey("Criterion", default="")
    option = models.ForeignKey("Option", default="")
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.option.name + " " + self.criterion.name + " " + str(self.number) + " by " + self.ratername

class FinalVote(models.Model):
    ratername = models.CharField(max_length=1000, default="")
    option = models.ForeignKey("Option", default="")


#below is some garbage that I threw out in the process of writing this app. 
#they are here just in case I need them in the future
'''
class Goal(models.Model):
    gcontent = models.CharField(max_length=1000)

    def __eq__(self, other):
        return self.gcontent == other.gcontent

    def __str__(self):
        return self.gcontent
'''
