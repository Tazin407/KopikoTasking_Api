from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, PermissionsMixin

PRIORITY= (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class CustomUser(AbstractUser,PermissionsMixin):
    username= models.CharField(unique=True, max_length= 10)
    first_name= models.CharField(max_length= 20)
    last_name= models.CharField(max_length= 20)
    email= models.EmailField()
    password= models.CharField(max_length= 50)
    is_active= models.BooleanField(default= False)
    
    def __str__(self) -> str:
        return self.username

class Category(models.Model):
    user= models.ForeignKey(CustomUser, on_delete= models.CASCADE)    
    title= models.CharField(max_length= 30)
    
    def __str__(self) -> str:
        return self.title

class Task(models.Model):
    user= models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    title= models.CharField(max_length= 200)
    slug= models.SlugField(max_length= 200, default="", null=False)
    description= models.TextField(blank= True)
    due_date= models.DateField()
    priority= models.IntegerField(choices= PRIORITY)
    Category= models.ForeignKey(Category, on_delete= models.CASCADE)
    is_completed= models.BooleanField(blank=True, default=False)
    
    def __str__(self) -> str:
        return self.title
    
    

    
    
    
    