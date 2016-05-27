from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your models here.

class MyUser(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(upload_to = 'profile_pics/', null = True, blank = True,)

# def upload_location(instance, filename):
#     filebase, extension = filename.split(".")
#     return "%s/%s.%s" %(instance.id, filename)

# class IssueManager(models.Manager):
#     def active(self, *args, **kwargs):
#         return super((IssueManager,self).filter(isChecked=False))


class Issue(models.Model):
    title = models.CharField(max_length=200, default='')
    text = models.TextField(max_length=2000, default='')
    image = models.ImageField(upload_to='postIssue/',
                              null = True,
                              blank = True,)
                              #height_field="height_field", 
                              #width_field="width_field")
    #height_field = models.IntegerField(default=0)
    #width_field = models.IntegerField(default=0)
    isChecked = models.BooleanField(default=False)
    #publish = models.DateField(auto_now=False, auto_now_add=False)
    created_on = models.DateTimeField(auto_now=True)
    last_checked = models.DateTimeField(auto_now_add=True)
    TEAMS_AND_CO_CURRICS = 'TNC'
    HOSTELS= 'HO'
    ACADEMICS= 'AC'
    ADMIN_DEALINGS = 'AD'
    MISCELLANEOUS='MS'
    CATEGORY = (
        (TEAMS_AND_CO_CURRICS, 'Teams-And-Co-Currics'),
        (HOSTELS, 'Hostels'),
        (ACADEMICS, 'Academics'),
        (ADMIN_DEALINGS, 'Admin-Dealings'),
        (MISCELLANEOUS, 'Miscellaneous'),
    )
    category = models.CharField(max_length=15, choices=CATEGORY, default=MISCELLANEOUS)
    raised_by = models.ForeignKey('MyUser',related_name = 'issues_raised', default='')
    upvoted_by = models.ManyToManyField('MyUser',related_name = 'upvoted', through='Upvote')
    #objects = IssueManager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("postIssue:get", kwargs={"id":self.id})

    class Meta:
        ordering = ["-last_checked", "-created_on"]

class Upvote(models.Model):
    user = models.ForeignKey(MyUser)
    issue = models.ForeignKey(Issue)
    is_upvoted =  models.BooleanField(default=False)
    

class Solution(models.Model):
    text = models.TextField(max_length=2000, default='')    
    created_on = models.DateTimeField(auto_now=True)
    last_checked = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('Issue', related_name = 'solutions', default='')
    posted_by = models.ForeignKey('MyUser', related_name = 'solutions_posted', default='') 

  
