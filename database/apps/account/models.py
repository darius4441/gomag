import os

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# from apps.base.father import PyFather
from apps.base.rename_image import RenameImage
from apps.contacts.models import Contact


def image_path(instance, filename):
    return os.path.join('avatar', str(instance.pk) + '.' + filename.rsplit('.', 1)[1])


class CustomAccountManager(BaseUserManager):
    def create_superuser(
        self, email, username, first_name, last_name, phone, password, **other_fields
    ):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            email, username, first_name, last_name, phone, password, **other_fields
        )

    def create_user(
        self, email, username, first_name, last_name, phone, password, **other_fields
    ):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(_("Name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True, null=True)
    email = models.CharField(_("Email"), max_length=254, null=False, db_index=True, unique=True)
    username = models.CharField(_("username"), max_length=70, unique=True)
    phone = models.CharField(_("Phone"), max_length=255, blank=True, null=True)
    mobile = models.CharField(_("Mobile Phone"), max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(_("start date"), default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(_("Staff"), default=False, db_index=True)
    is_active = models.BooleanField(_("Active"), default=False)
    avatar = models.ImageField(max_length=255, storage=RenameImage(), upload_to=image_path, blank=True, null=True, default='avatar/default_avatar.png')
    contact_id = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT)
    # active_company = models.ForeignKey('base.PyCompany', on_delete=models.PROTECT)
    password = models.CharField(_("Password"), max_length=128)
    last_login = models.DateTimeField(_("Last login"), default=timezone.now)
    is_superuser = models.BooleanField(_("Super Admin"), default=False, db_index=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ["-start_date"]

        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    def __str__(self):
        return self.username

    @classmethod
    def create(cls, first_name, last_name, email, password,  is_superuser, is_staff, is_active, active_company):      
        contact_name = '{} {}'.format(first_name, last_name)
        contact = Contact.create(contact_name, email)
        newuser = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            active_company=active_company,
            company_id=active_company.id,
            contact_id=contact,
        )
        newuser.set_password(password)
        newuser.save()

        return newuser

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        db_table = 'auth_user'




"""
import os
from tabnanny import verbose

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.base.rename_image import RenameImage
from apps.contacts.models import Contact


def image_path(instance, filename):
    return os.path.join('avatar', str(instance.pk) + '.' + filename.rsplit('.', 1)[1])


class CustomAccountManager(BaseUserManager):
    def create_superuser(
        self, email, username, first_name, last_name, phone, password, **other_fields
    ):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            email, username, first_name, last_name, phone, password, **other_fields
        )

    def create_user(
        self, email, username, first_name, last_name, phone, password, **other_fields
    ):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractUser):
    '''Modelo de los usuarios
    '''
    SEXO_CHOICES = (
        ('F', _('FEMALE')),
        ('M', _('MALE')),
    )
    LETRACEDULA_CHOICES = (
        ('V', 'V'),
        ('E', 'E'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(_("Name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True, null=True)
    email = models.CharField(_("Email"), max_length=254, null=False, db_index=True, unique=True)
    username = models.CharField(_("username"), max_length=70, unique=True)
    phone = models.CharField(_("Phone"), max_length=255, blank=True, null=True)
    mobile = models.CharField(_("Mobile Phone"), max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(_("start date"), default=timezone.now)
    about = models.TextField(_("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(_("Staff"), default=False, db_index=True)
    is_active = models.BooleanField(_("Active"), default=False)
    avatar = models.ImageField(max_length=255, storage=RenameImage(), upload_to=image_path, blank=True, null=True, default='avatar/default_avatar.png')
    contact_id = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.PROTECT)
    active_company = models.ForeignKey('base.PyCompany', on_delete=models.PROTECT)
    password = models.CharField(_("Password"), max_length=128)
    last_login = models.DateTimeField(_("Last login"), default=timezone.now)
    is_superuser = models.BooleanField(_("Super Admin"), default=False, db_index=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return '%s %s' % (self.first_name, self.last_name)


    @classmethod
    def create(cls, first_name, last_name, email, password,  is_superuser, is_staff, is_active, active_company):      
        contact_name = '{} {}'.format(first_name, last_name)
        contact = Contact.create(contact_name, email)
        newuser = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            active_company=active_company,
            company_id=active_company.id,
            contact_id=contact,
        )
        newuser.set_password(password)
        newuser.save()

        return newuser

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        db_table = 'auth_user'

"""
