from django.db import models
from users.models import User

class List(models.Model):
    name = models.CharField(max_length=15)
    color = models.CharField(max_length=15, default='default')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists', default=1)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, default=None, null=True)
    status = models.BooleanField(default=False)
    created_at = models.CharField(max_length=20)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

# class Subnote(models.Model):
#     title = models.CharField(max_length=200)
#     status = models.BooleanField(default=False)
#     note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='subnotes', null=True, blank=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)


#     def __str__(self):
#         return self.title