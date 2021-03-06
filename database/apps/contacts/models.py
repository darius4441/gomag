import os

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.base.rename_image import RenameImage

TYPE_CHOICE = (
    ("company", _("Company")),
    ("individual", _("Individual")),
    ("address", _("Address")),
    ("contact", _("Contact")),
)

_UNSAVED_FILEFIELD = 'unsaved_filefield'


def image_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return "partner/{id}{ext}".format(id=instance.pk, ext=ext)

class Contact(models.Model):
    name = models.CharField(_("Name"), max_length=40)
    street = models.CharField(_("Street"), max_length=100, blank=True)
    street_2 = models.CharField(_("Street Other"), max_length=100, blank=True)
    city = models.CharField(_("City"), max_length=50, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), max_length=40, blank=True)
    is_customer = models.BooleanField(_("Customer"), default=True)
    is_provider = models.BooleanField(_("Provider"), default=True)
    is_for_invoice = models.BooleanField(_("For Invoice"), default=True)
    note = models.TextField(blank=True, null=True)
    has_not_email = models.BooleanField(_("No Email"), default=False)
    parent_id = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        verbose_name=_('Parent du contact')
    )
    img = models.ImageField(
        max_length=255,
        storage=RenameImage(),
        upload_to=image_path,
        blank=True,
        null=True,
        default='contact/default_partner.png'
    )
    type = models.CharField(
        _("type"),
        choices=TYPE_CHOICE,
        max_length=64,
        default='company'
    )

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, email):
        pypartner = cls(name=name, email=email)
        pypartner.save()
        return pypartner

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


@receiver(pre_save, sender=Contact)
def skip_saving_file(sender, instance, **kwargs):
    if not instance.pk and not hasattr(instance, _UNSAVED_FILEFIELD):
        setattr(instance, _UNSAVED_FILEFIELD, instance.img)
        instance.img = 'partner/default_partner.png'


@receiver(post_save, sender=Contact)
def save_file(sender, instance, created, **kwargs):
    if created and hasattr(instance, _UNSAVED_FILEFIELD):
        instance.img = getattr(instance, _UNSAVED_FILEFIELD)
        instance.save()
        instance.__dict__.pop(_UNSAVED_FILEFIELD)
    if not instance.img or instance.img is None:
        instance.img = 'contact/default_partner.png'
        instance.save()
