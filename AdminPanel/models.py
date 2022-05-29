from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SendEmailToUser(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sen")
    receiver = models.CharField(max_length=220, null=True)
    subject = models.CharField(max_length=220)
    content = models.TextField()
    attachment = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return str(self.id)