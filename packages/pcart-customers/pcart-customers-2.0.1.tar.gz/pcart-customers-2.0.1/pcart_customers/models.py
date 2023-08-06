from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.urls import reverse, NoReverseMatch
from django.conf import settings
import uuid

from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email, phone, password and optional extra info.
    """
    def _create_user(self, email, phone, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')
        if not phone:
            raise ValueError('The given phone must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            last_login=now,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password=None, **extra_fields):
        return self._create_user(email, phone, password, False, False, **extra_fields)

    def create_superuser(
            self, email, phone, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email,
        phone and password.
        """
        return self._create_user(email, phone, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A model which implements the authentication model.

    Email, password and phone are required. Other fields are optional.

    Email and phone fields are used for logging in.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    phone = models.CharField(_('Phone'), max_length=100, unique=True)

    data = JSONField(_('Data'), default=dict, blank=True)

    is_staff = models.BooleanField(
        _('Staff status'), default=False, blank=True,
        help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('Active'), default=True, blank=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.data.get('full_name', self.email)

    def get_full_name(self):
        return self.data.get('full_name', self.email)

    def get_short_name(self):
        return self.data.get('full_name', self.email)

    def get_email_md5_hash(self):
        import hashlib
        m = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return m

    def has_usable_password(self):
        return super().has_usable_password()
    has_usable_password.boolean = True


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        verbose_name=_('User'),
        null=True, blank=True, on_delete=models.CASCADE,
        related_name='customer',
    )
    session_id = models.CharField(_('Session ID'), default='', blank=True, max_length=100)

    name = models.CharField(_('Name'), default='', blank=True, max_length=255)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return '%s' % (self.user or self.id)


class PasswordResetLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(_('Slug'), unique=True, max_length=120, blank=True)
    user = models.OneToOneField(
        User,
        verbose_name=_('User'), on_delete=models.CASCADE, related_name='password_reset_link',
    )
    active = models.BooleanField(_('Active'), default=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    expiration_date = models.DateTimeField(_('Expiration date'))

    class Meta:
        verbose_name = _('Password reset link')
        verbose_name_plural = _('Password reset links')

    def __str__(self):
        return '%s' % self.user

    def save(self, *args, **kwargs):
        from django.utils import timezone
        from datetime import timedelta

        if not self.slug:
            import uuid
            self.slug = uuid.uuid4().hex

        if not self.expiration_date:
            now = timezone.now()
            self.expiration_date = now + timedelta(days=355)

        super(PasswordResetLink, self).save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('pcart_customers:password-reset-confirm', args=[self.slug])
        except NoReverseMatch:
            return '#no-page-for-customers-app'

    def send_message(self, extra_context={}):
        """Send an email with a reset link."""
        from pcart_messaging.utils import create_email_message
        from django.contrib.sites.models import Site
        from django.conf import settings
        sender = settings.DEFAULT_FROM_EMAIL
        site = Site.objects.get_current()
        context = {
            'reset_link': self,
            'site': site,
        }
        context.update(extra_context)
        recipients = [self.user.email]

        email_template_name = 'reset_password' if self.user.has_usable_password() else 'setup_password'
        msg = create_email_message(email_template_name, recipients, sender, context)
        msg.send()
