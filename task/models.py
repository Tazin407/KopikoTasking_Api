from django.db import models

# Create your models here.
from django.contrib.auth.models import User

PRIORITY= (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class Category(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)    
    title= models.CharField(max_length= 30)
    
    def __str__(self) -> str:
        return self.title

class Task(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    slug= models.SlugField(max_length= 200, default="", null=False)
    description= models.TextField(blank= True)
    due_date= models.DateField()
    priority= models.IntegerField(choices= PRIORITY)
    Category= models.ForeignKey(Category, on_delete= models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    
    
    
    