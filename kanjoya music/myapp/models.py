from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Facts(models.Model):
    text = models.CharField(max_length=70)
    def __unicode__(self):
       return self.text

class UserFacts(models.Model):
    user = models.ForeignKey(User)
    fact = models.ForeignKey(Facts)
    def __unicode__(self):
       return self.user.username + ' : ' + self.fact.text

