from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    # NOTE:
    # After "objects = UserManager()" in the User class,
    # The self.model() is assigned User() in the User class.
    def create_user(
        self, email, password=None, name="", is_active=True, is_staff=False
    ):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(
            # NOTE: normalize_email is a method of BaseUserManager
            email=self.normalize_email(email),
            name=name,
            is_active=is_active,
            is_staff=is_staff,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # NOTE: Every Django model has at least one manager,
    # and the default manager is called objects.
    # By this line replacing the default manager with custom one
    objects = UserManager()

    # NOTE:
    # Custom option provided by Django, other more
    # https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser
    USERNAME_FIELD = "email"
