from django.contrib import admin
from .import models
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display= ['username', 'title']
    prepopulated_fields = {"slug": ("title",)}
    
    def username(self, obj):
        return obj.user.username
    
admin.site.register(models.Category)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.CustomUser)
    
    