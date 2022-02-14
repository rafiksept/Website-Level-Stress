from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from httpx import delete
from numpy import require
# Create your models here.

class Gambar(models.Model):
    author  = models.CharField(max_length=255, blank=True)
    foto    = models.ImageField(upload_to='cover/', null=True)
    user    = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id},{self.author}'
    
    def get_absolute_url(self):
        return f"/foto/"



class Cerita(models.Model):
    judul   = models.CharField(max_length=255)
    isi     = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    slug    = models.SlugField(blank=True, editable=False)
    author  = models.CharField(max_length=255, blank=True)
    stress  = models.IntegerField(blank=True, editable=False, null=True)
    is_publish = models.BooleanField(blank=False)
    anonymous = models.BooleanField(blank=False)
    gambar = models.ForeignKey(Gambar,default=25, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def save(self):
        self.slug = slugify(self.judul)
        super().save()
    
    def __str__(self):
        return f'{self.id}.{self.judul}'

class Komentar(models.Model):
    author   = models.CharField(max_length=255, blank=True)
    coment   = models.TextField(blank=False)
    anonymous = models.BooleanField(blank=False)
    publish = models.DateTimeField(auto_now_add=True, blank=True)
    postingan = models.ForeignKey(Cerita,  on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    gambar = models.ForeignKey(Gambar,default=25, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return f'{self.id}.{self.coment}'