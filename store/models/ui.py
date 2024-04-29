from winreg import QueryInfoKey
from django.db import models


class UI(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(default="",upload_to='uploads/ui/')
    video = models.FileField(default="", upload_to='uploads/video/')
    @staticmethod
    def get_element_by_name(name):
        if name:
            return UI.objects.get(name=name)
        else:
            return None
