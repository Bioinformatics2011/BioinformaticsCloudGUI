from django.db import models
import os.path

def content_file_name(instance, filename):
    return '/'.join([instance.userName, filename])


class UserFile(models.Model):
    userFile = models.FileField(upload_to=content_file_name)
    userName = models.CharField(max_length=30)
    
    def filename(self):
        return os.path.basename(self.userFile.name)
        