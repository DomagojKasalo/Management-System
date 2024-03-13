from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Uloge(models.Model):
    ADMIN = 'ADMIN'
    PROFESOR =  'PROFESOR'
    STUDENT  = 'STUDENT'
    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (PROFESOR, 'profesor'),
        (STUDENT, 'student'),
    ]
    uloga = models.CharField(choices=ROLE_CHOICES, max_length=20, null=True)

    def __str__(self):
        return '%s' % (self.uloga)

class Korisnik(AbstractUser):
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length=50, choices=STATUS)
    uloge = models.ForeignKey(Uloge, on_delete=models.SET_NULL, null=True, blank=True, related_name='uloge')

class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.SET_NULL, null=True, blank=True, related_name='nositelj')
    upisi = models.ManyToManyField(Korisnik, through='Upis', related_name='predmeti_upis')

    def __str__(self):
        return '%s' % (self.name)


class Upis(models.Model):
    student_id = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=True, related_name='student')
    predmet_id = models.ForeignKey(Predmeti, on_delete=models.CASCADE, null=True, related_name='predmet')
    STATUS = (('upisan','Upisan'),('polozen','Polozen'),('izgubio potpis','Izgubio potpis'))
    status = models.CharField(max_length=50, choices=STATUS)
