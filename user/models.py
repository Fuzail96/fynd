from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
import uuid
import jwt


JWT_SECRET = settings.JWT_SECRET

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self, password, email="admin", **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    unique_id = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField(_("Email address"), default="", blank=True, unique=True)
    phone = models.CharField(_("Mobile Number"), max_length=17, unique=True)
    name = models.CharField(_("Full name"), max_length=40, blank=True)
    # Permissions
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is admin"), default=False)
    # Meta
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def verify_token(cls, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
            uid = payload["unique_id"]
            return User.objects.only('unique_id').get(unique_id=uid)
        except User.DoesNotExist:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None

    def token(self):
        secret = JWT_SECRET
        return jwt.encode({'unique_id': str(self.unique_id)}, secret, algorithm='HS256')


