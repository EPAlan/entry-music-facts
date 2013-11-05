from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.

class Fact(models.Model):
    text = models.CharField(max_length=70)
    def __unicode__(self):
        return self.text

class Kanjoyan(models.Model):
    firstname = models.CharField(max_length=50)
    lastname= models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    randomKey = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def image(self):
        filename = os.path.dirname(os.path.realpath(__file__)) + '/static/images/' + self.username + '.jpg'
        try:
            f = open(filename)
            f.close()
            return 'static/images/' + self.username + '.jpg'
        except IOError:
            filename = 'static/images/default.jpg'
        return filename

    def __unicode__(self):
        return str(self.id) + ' : ' + self.username

class UserFact(models.Model):
    kanjoyan = models.ForeignKey(Kanjoyan)
    fact = models.ForeignKey(Fact)
    def __unicode__(self):
        return self.kanjoyan.username + ' : ' + self.fact.text

class Score(models.Model):
    kanjoyan = models.ForeignKey(Kanjoyan)
    score = models.IntegerField(default=0)
    def __unicode__(self):
        return self.kanjoyan.username + ' : ' + str(self.score)


