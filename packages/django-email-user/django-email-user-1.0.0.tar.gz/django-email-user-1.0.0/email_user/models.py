from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.six import python_2_unicode_compatible, text_type


class EmailUserQuerySet(models.query.QuerySet):
    def _filter_or_exclude(self, *args, **kwargs):
        """ Make email lookups case-insensitive """
        if 'email' in kwargs:
            kwargs['email__iexact'] = kwargs.pop('email')
        return super(EmailUserQuerySet, self)._filter_or_exclude(*args, **kwargs)

    def active(self):
        return self.filter(is_active=True)


class EmailUserManager(BaseUserManager):
    def get_queryset(self):
        return EmailUserQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.validate_unique()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.validate_unique()
        user.save(using=self._db)
        return user

    def active(self):
        return self.get_queryset().active()


@python_2_unicode_compatible
class EmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, max_length=255, db_index=True)
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = EmailUserManager()

    class Meta:
        abstract = True
        ordering = ('email',)

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return ''
        return text_type(' ').join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
