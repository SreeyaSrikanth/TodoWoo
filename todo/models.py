from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=70)
    memo = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    due_time = models.DateTimeField()
    complete_time = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title