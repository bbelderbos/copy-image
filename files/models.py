import os

from django.db import models

from .aws import create_presigned_url


class Attachment(models.Model):
    url = models.URLField()
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    @property
    def signed_url(self):
        object_name = os.path.basename(self.url)
        return create_presigned_url(object_name)

    @property
    def filename(self):
        return os.path.basename(self.url)
