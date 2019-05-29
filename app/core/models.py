from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, full_name, email, password=None, is_active=True, is_staff=False, is_superuser=False, **extra_fields):
        if not full_name:
            raise ValueError("User must have full name")
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) #how to change user password
        user_obj.staff = is_staff
        user_obj.admin = is_superuser
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, full_name, email, password=None):
        user = self.create_user(
            full_name,
            email,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(
            full_name,
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        ) #test
        return user
    
    
    
    


class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(max_length=255, unique=True) #email
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    password    = models.CharField(max_length=50, unique=True) #password
    active   = models.BooleanField(default=True) #can log in
    staff    = models.BooleanField(default=False) #part of staff
    admin       = models.BooleanField(default=False) #superuser 

    USERNAME_FIELD = 'email' #email is the username rather than writing additional code

    REQUIRED_FIELDS = []  

    objects = UserManager()


    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Step(models.Model):
    """Step to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title



    

    