from django.db import models
from localflavor.br import models as localModels
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass


class Customer(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'


class Company(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comapnies')

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'


class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')

    class Meta:
        permissions = (('read_project', 'Read Project'),)

    def __str__(self):
        return self.name


class House(models.Model):
    rooms = models.IntegerField()
    postal_code = localModels.BRPostalCodeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
