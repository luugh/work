from django.db import models

# Create your models here.

class channel():
    cpcode = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    str_staus = models.CharField(max_length=10)
    cdn_status = models.CharField(max_length=10)
    list_status = models.CharField(max_length=10)