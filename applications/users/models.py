import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.tenant.models import Tenant
from applications.vehicles.models import Vehicle

PASSWORD_LENGTH = 8


class Role(models.TextChoices):
    """
    Admin has access to mobile app and admin web site.
    User has access only to mobile app.
    """
    ADMIN = 'ADMIN', _('Admin'),
    USER = 'USER', _('User')


class MyUserManager(BaseUserManager):
    def create_user(self, email, fullname, tenant, password=None):
        try:
            tenant = Tenant.objects.get(id=tenant)
        except ValidationError:
            raise ValueError('Tenant UUID not valid. Use "python manage.py showtenants" to see ids')
        except Tenant.DoesNotExist:
            raise ValueError('Tenant does not exists. Use "python manage.py showtenants" to see ids')

        if not email:
            raise ValueError('Users must have an email address.')
        if not fullname:
            raise ValueError('Users must have a fullname.')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
        )
        user.tenant = tenant
        user.role = Role.USER
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, tenant, password=None):

        user = self.create_user(
            email,
            fullname=fullname,
            tenant=tenant,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = Role.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    fullname = models.CharField(verbose_name='fullname', max_length=70)
    tenant = models.ForeignKey(Tenant, related_name='users', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)

    allowed_vehicles = models.ManyToManyField(
        Vehicle,
        through='allowed_vehicles.AllowedVehicles',
        through_fields=('user', 'vehicle'),
        related_name='allowed_vehicles'
    )

    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'tenant']

    objects = MyUserManager()

    def __str__(self):
        return '{} ({})'.format(self.fullname, self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'User'


CODE_LENGTH = 6


class RecoverPasswordStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    COMPLETED = 'COMPLETED', _('Completed')


class RecoverPassword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_stored = models.DateTimeField(auto_now_add=True)
    code = models.CharField(
        max_length=CODE_LENGTH,
        validators=[MinLengthValidator(CODE_LENGTH)],
        unique=False
    )
    status = models.CharField(
        max_length=9,
        choices=RecoverPasswordStatus.choices,
        default=RecoverPasswordStatus.PENDING
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recover_passwords', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, related_name='recover_passwords', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Recover Password'
        ordering = ['-date_stored']

    def __str__(self):
        return '{} - {}'.format(self.code, self.status)
