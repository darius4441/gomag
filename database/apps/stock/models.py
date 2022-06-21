# Django Library
import glob
import os
from io import BytesIO
from itertools import product
from unicodedata import category

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from apps.account.models import NewUser

from .utils import slugify_instance_name

PRODUCT_CHOICE = (
    ("storable", "Storable product"),
    ("service", "Service"),
    ("consumable", "Consumable"),
)

TYPE_CHOICE = (
    ("bigger", "Bigger"),
    ("reference", "Reference"),
    ("smaller", "Smaller"),
)


# ******************************************************************************


def image_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return "product/{id}{ext}".format(id=instance.pk, ext=ext)


# ******************************************************************************


class RenameImage(FileSystemStorage):
    """Returns a filename that's free on the target storage system, and
    available for new content to be written to.

    Found at http://djangosnippets.org/snippets/976/"""

    def get_available_name(self, name, max_length=None):
        """This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):
        """
        # If the filename already exists with any ext, remove it as if it was
        # a true file system
        root, ext = os.path.splitext(name)
        name_to_delete = "{}{}{}{}".format(
            settings.BASE_DIR, settings.MEDIA_URL, root, "*"
        )
        for filename in glob.glob(name_to_delete):
            os.remove(filename)

        return name


# ******************************************************************************


class ParentUOM(models.Model):
    name = models.CharField(_("catégorie"), max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Groupe d'unité")
        verbose_name_plural = _("Groupe d'unités")


# ******************************************************************************


class Uom(models.Model):
    name = models.CharField(_("libellé"), max_length=255)
    ratio = models.DecimalField(
        _("ratio"), max_digits=10, decimal_places=2, default=1
    )
    rouding = models.DecimalField(
        _("arrondi au"), max_digits=10, decimal_places=2, default=0.01
    )
    type = models.CharField(
        _("type"), choices=TYPE_CHOICE, max_length=64, default="reference"
    )
    uom_parent = models.ForeignKey(
        ParentUOM,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.uom_parent.name} - {self.name}"

    class Meta:
        verbose_name = _("Unité de mesure")
        verbose_name_plural = _("Unité de mesures")


# ******************************************************************************


class ProductCategory(models.Model):
    name = models.CharField(_("nom"), max_length=40)
    parent = models.ForeignKey(
        "self", null=True, blank=True, default=None, on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Catégorie de produit"
        verbose_name_plural = "Catégories de produit"

    def __str__(self):
        return "%s" % (self.name)


# ******************************************************************************


class Product(models.Model):
    name = models.CharField(_("name"), max_length=80)
    prod_type = models.CharField(
        _("type"), choices=PRODUCT_CHOICE, max_length=64, default="storable"
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name="product_cats",
        verbose_name=("catégorie d'article"),
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default=1,
    )
    isArchived = models.BooleanField(_("est archivé"), default=False)
    code = models.CharField(_("code"), null=True, blank=True, max_length=80)
    description = models.TextField(_("description"), blank=True, null=True)
    photo_url = models.ImageField(
        _("photo"),
        storage=RenameImage(),
        upload_to=image_path,
        blank=True,
        null=True,
        default="product/default_product.png",
    )
    thumbnail = models.ImageField(
        storage=RenameImage(),
        upload_to=image_path,
        blank=True,
        null=True,
    )
    uom = models.CharField(_("unité de mesure"), max_length=30)
    unit = models.ForeignKey(
        Uom,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="futur unité de mesure",
    )
    providers = models.CharField(
        _("fournisseurs"), max_length=120, null=True, blank=True
    )
    real_quantity = models.FloatField(_("stock réel"), default=0)
    virtual_quantity = models.FloatField(_("stock virtuel"), default=0)
    unit_price = models.FloatField(_("prix de vente"), default=1)
    semi_wholesale_price = models.FloatField(_("prix de demi-gros"), default=1)
    wholesale_price = models.FloatField(_("prix de gros"), default=1)
    unit_cost = models.FloatField(_("cout d'achat"), default=1)
    alert_stock = models.IntegerField(_("qté alerte"), default=0)
    optimal_stock = models.IntegerField(_("qté idéale"), default=0)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(
        NewUser,
        related_name="created_products",
        on_delete=models.CASCADE,
        verbose_name="créer par",
    )
    modified_by = models.ForeignKey(
        NewUser,
        related_name="modified_products",
        on_delete=models.CASCADE,
        verbose_name="modifié par",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="créer le"
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name="modifié le"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    @classmethod
    def suma(cls):
        return cls.__name__

    def __str__(self):
        return f"{self.name}"

    def isAlert(self):
        if self.real_quantity <= self.alert_stock:
            return True
        else:
            return False

    def getReplenish(self):
        if self.optimal_stock:
            return self.optimal_stock - self.real_quantity
        return 0

    def getUom(self):
        return self.uom

    def get_category(self):
        return "%s" % (self.category.name)

    def get_absolute_url(self):
        # return f'/products/{self.slug}/'
        return reverse("products:detail", kwargs={"slug": self.slug})

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url

        else:
            if self.photo_url:
                self.thumbnail = self.make_thumbnail(self.photo_url)
                self.save()

                return self.thumbnail.url
            else:
                return "http://via.placeholder.com/240x240x.jpg"

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


pre_save.connect(product_pre_save, sender=Product)


def product_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_name(instance, save=True)


post_save.connect(product_post_save, sender=Product)

# ******************************************************************************


class Inventory(models.Model):
    name = models.CharField(_("libellé"), max_length=80)
    isApply = models.BooleanField(_("est appliqué"), default=False)
    date = models.DateField(_("date"))

    created_by = models.ForeignKey(
        NewUser,
        related_name="created_inventories",
        on_delete=models.CASCADE,
        verbose_name="créer par",
    )
    modified_by = models.ForeignKey(
        NewUser,
        related_name="modified_inventories",
        on_delete=models.CASCADE,
        verbose_name="modifié par",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="créer le"
    )
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name="modifié le"
    )

    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"

    def __str__(self):
        return format(self.name)


# ******************************************************************************


class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        related_name="items_inventory",
        on_delete=models.CASCADE,
        verbose_name="inventaire",
    )
    article = models.ForeignKey(
        Product,
        related_name="items_product",
        on_delete=models.CASCADE,
        verbose_name="article",
    )
    initial_quantity = models.FloatField(
        _("initial quantity"),
        blank=True,
        null=True,
        default=0,
    )

    def getArticleName(self):
        return self.article.name

    def getArticleUom(self):
        return self.article.uom
