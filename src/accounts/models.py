from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if email is None:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None:
            raise ValueError('Superusers must have a password.')
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 15, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    news_labeled =  models.CharField(max_length = 4000)
    favorite = models.CharField(max_length = 400)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username
