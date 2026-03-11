from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class Role:
    admin = 'admin'
    user = 'user'
    choices = [
        (admin, 'Admin'),
        (user, 'User'),
    ]



class ALX_STATUS:
    alumni = 'alumni'
    learner = 'learner'
    guest = 'guest'
    choices = [
        (alumni, 'Alumni'),
        (learner, 'Learner'),
        (guest,'guest'),
    ]




class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=100,null=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.user)
    phone_no = models.CharField(max_length=11,null=False,blank=False)
    user_status = models.CharField(choices=ALX_STATUS.choices,max_length=50,blank=False,null=False)
    city = models.CharField(max_length=100,null=False,blank=False)



    objects = UserManager()
