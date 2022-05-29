from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import NewUser

CHOICE_GENDER = (("mr", "Monsieur"), ("mme", "Madame"))

CHOICE_CONTACT_TYPE = (
    ("company", "Entreprise"),
    ("deliver", "Livreur"),
    ("client", "Client"),
)


class Company(models.Model):
    name = models.CharField(_("nom"), max_length=50)
    phone = models.CharField(_("téléphone"), max_length=10)
    email = models.EmailField(_("email"), blank=True, null=True)
    created_at = models.DateTimeField(_("Créer le"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modifier le"), auto_now=True)
    created_by = models.ForeignKey(
        NewUser, related_name="created_companies", on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        NewUser, related_name="modified_companies", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(_("nom"), max_length=50)
    gender = models.CharField(
        _("genre"),
        choices=CHOICE_GENDER,
        default="mr",
        max_length=3,
    )
    company = models.ForeignKey(
        Company,
        related_name="company_contact",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    c_type = models.CharField(
        _("type de contact"),
        max_length=7,
        choices=CHOICE_CONTACT_TYPE,
        default="client",
    )
    is_archived = models.BooleanField(_("est archivé"), default=False)
    created_at = models.DateTimeField(_("Créer le"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modifier le"), auto_now=True)
    created_by = models.ForeignKey(
        NewUser, related_name="created_contacts", on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        NewUser, related_name="modified_contacts", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def getCompanyName(self):
        return self.company.name
