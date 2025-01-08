from django.db import models
from django.contrib.auth.models import User

# This code is for referencing only. It is not used in the project.
# class Note(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
# This code above is for referencing only. It is not used in the project.

class Profile(models.Model):
    # Write in the future

    def __str__(self):
        return self.title
