from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import NewUser
from apps.contacts.models import Contact
from apps.stock.models import Product


class Operation(models.Model):
    TYPE_CHOICE = (
        ("in", "Entrée"),
        ("out", "Sortie"),
        ("rtn", "Retour"),
    )
    STATE_CHOICE = (
        ("draft", "Brouillon"),
        ("pending", "En cours"),
        ("done", "Fait"),
    )
    operation_number = models.IntegerField(_("operation number"), default=1)
    state = models.CharField(
        _("operation state"),
        max_length=7,
        choices=STATE_CHOICE,
        default="draft",
    )
    contact = models.ForeignKey(
        Contact, related_name="contact_operations", on_delete=models.CASCADE
    )
    m_type = models.CharField(
        _("operation type"),
        max_length=3,
        choices=TYPE_CHOICE,
        default="out",
    )
    date = models.DateField(_("date"), max_length=255)
    annexe = models.CharField(
        _("document annexe of this operation"),
        max_length=255,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        NewUser, related_name="created_operations", on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        NewUser, related_name="modified_operations", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Opération")
        verbose_name_plural = _("Opérations")

    def __str__(self):
        return f"Command of : {self.contact}"

    def getContactName(self):
        return self.contact.name


class Item(models.Model):
    operation = models.ForeignKey(
        Operation, related_name="items", on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Product, related_name="articles", on_delete=models.PROTECT
    )
    quantity = models.FloatField(_("quantity"), default=1)
    unit = models.CharField(_("unit"), max_length=30)
    old_qty = models.FloatField(_("ancienne quantité"), blank=True, null=True)
    cost = models.FloatField(_("cout d'achat"), blank=True, null=True)

    def __str__(self):
        return f"{self.article.name} item of operation#{self.operation.operation_number}"

    def get_article_name(self):
        return f"{self.article.name}"

    def get_article_available_qty(self):
        return f"{self.article.real_quantity}"
