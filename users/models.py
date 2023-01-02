from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Portal(models.Model):

    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.CharField(choices=SEX, max_length=6, null=True, blank=True, default=None)
    staff_num = models.CharField(max_length=15)
    phone_number = models.IntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.staff.username + ' | ' + str(self.phone_number)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


class Student(models.Model):

    LEVEL = (
        (100, 100),
        (200, 200),
        (300, 300),
        (400, 400),
        (500, 500),
        (600, 600),
        (700, 700),
    )

    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    SPACE = (
        ('UP', 'UP'),
        ('DOWN', 'DOWN'),
        ('', ''),
    )

    stud = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.CharField(choices=SEX, max_length=6)
    mat_no = models.CharField(max_length=15)
    department = models.CharField(max_length=30)
    level = models.IntegerField(choices=LEVEL)
    school_fees = models.FileField(upload_to=f'student/school_fees')  # upload to cloudinary
    hostel_application = models.FileField(upload_to=f'student/hostel_application')  # upload to cloudinary
    profile_image = models.ImageField(blank=True, null=True, upload_to=f'student/images')
    booking = models.BooleanField(default=False)
    space = models.CharField(choices=SPACE, max_length=5, null=True, blank=True, default=None)
    slug = models.SlugField()

    def __str__(self):
        return self.mat_no + ' | ' + str(self.stud.username)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})


# Create your models here.
