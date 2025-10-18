from django.db import models
from django.contrib.auth.models import BaseUserManager ,AbstractUser,PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email('email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password= None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email,password, **extra_fields)
    
class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=550,null=False,blank=False)
    full_name = models.CharField(max_length=150, null=False,blank=False)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(pre_save, sender=User)
def set_full_name(sender, instance, **kwargs):
    instance.full_name = f"{instance.first_name} {instance.last_name}".strip()