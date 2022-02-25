from time import timezone
from tkinter import CASCADE
from django.db import models
from django.utils import timezone
## Importing user table 
from django.contrib.auth.models import User
from django.urls import reverse 
# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=20)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
 
        return self.title

    ## cascade will delete the post as well
    
    ## It asks for absolute URL
    def get_absolute_url(self) :

        return reverse('post-detail',kwargs={'pk':self.pk})


    

