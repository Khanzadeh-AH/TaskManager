from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, fullname, username, email, is_active=True, is_staff=False, is_admin=False, password=None):
        if not fullname:
            raise ValueError("User must have a name")
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            fullname=fullname,
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, fullname, username, email, password):
        user = self.create_user(
            fullname=fullname,
            username=username,
            email=email,
            password=password,
            is_staff=True
        )

    def create_sueperuser(self, fullname, username, email, password):
        user = self.create_user(
            fullname=fullname,
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )


class CustomUser(AbstractBaseUser):
    fullname    = models.CharField(max_length=255)
    username    = models.CharField(max_length=255, unique=True)
    email       = models.EmailField(unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True)
    banned      = models.BooleanField(default=False)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = ['email']
    REQUIRED_FIELDS = ['fullname', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = "User"
