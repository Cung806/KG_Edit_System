from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from manageDomain.models import DomainModel
# Create your models here.


# class User(AbstractUser):
#     user_domain = models.ForeignKey(DomainModel, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.username


# class DomainUser(models.Model):
#     domainuserid = models.AutoField(primary_key=True)
#     domain_id = models.ForeignKey(DomainModel, on_delete= models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete= models.CASCADE)
#
#     def __str__(self):
#         return self.domainuserid
