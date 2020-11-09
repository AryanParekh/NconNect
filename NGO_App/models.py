from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NGOProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    registration_number=models.CharField(unique=True,max_length=10)
    ngo_name=models.CharField(max_length=50)
    certificate=models.ImageField(blank=False,upload_to='certificate_pics')
    image=models.ImageField(upload_to='ngo_images')
    description=models.TextField(max_length=1000)
    contact = models.CharField(max_length=10)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    verfied=models.BooleanField(default=False)
    address_line_1=models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    address_line_1=models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class NgoRequirements(models.Model):
    ngo = models.ForeignKey(NGOProfile,on_delete=models.CASCADE)
    requirement= models.CharField(max_length=60,null=False)
    quantity=models.IntegerField(null=False)
    message=models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)

class Reciept(models.Model):
    ngo = models.ForeignKey(NGOProfile,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    ngo_add_requirement = models.CharField(max_length=50)
    donated_items=models.IntegerField()

    def __str__(self):
        return str(self.id)
