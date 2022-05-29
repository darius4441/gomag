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


class CategoryUOM(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")


# ******************************************************************************


class Uom(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    ratio = models.DecimalField(
        _("Ratio"), max_digits=10, decimal_places=2, default=1
    )
    rouding = models.DecimalField(
        _("Ratio"), max_digits=10, decimal_places=2, default=0.01
    )
    type = models.CharField(
        _("type"), choices=TYPE_CHOICE, max_length=64, default="consu"
    )
    category_id = models.ForeignKey(
        CategoryUOM, null=True, blank=True, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Uom")
        verbose_name_plural = _("Uom")


# ******************************************************************************


class Product(models.Model):
    name = models.CharField(_("name"), max_length=80)
    prod_type = models.CharField(
        _("type"), choices=PRODUCT_CHOICE, max_length=64, default="storable"
    )
    category = models.CharField(
        _("category"), null=True, blank=True, max_length=40
    )
    isArchived = models.BooleanField(_("est archivé"), default=False)
    code = models.CharField(_("code"), null=True, blank=True, max_length=80)
    description = models.TextField(_("description"), blank=True, null=True)
    photo_url = models.ImageField(
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
    uom = models.CharField(_("Unit of measure"), max_length=30)
    providers = models.CharField(
        _("providers"), max_length=120, null=True, blank=True
    )
    # uom = models.ForeignKey(Uom, null=True, blank=True, on_delete=models.PROTECT)
    real_quantity = models.FloatField(_("real quantity"), default=0)
    virtual_quantity = models.FloatField(_("virtual quantity"), default=0)
    unit_price = models.FloatField(_("sale price"), default=1)
    unit_cost = models.FloatField(_("purchase cost"), default=1)
    alert_stock = models.IntegerField(_("alert stock"), default=0)
    optimal_stock = models.IntegerField(_("good stock"), default=0)
    slug = models.SlugField(blank=True, null=True)
    created_by = models.ForeignKey(
        NewUser, related_name="created_products", on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        NewUser, related_name="modified_products", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    @classmethod
    def suma(cls):
        return cls.__name__

    def __str__(self):
        return f"{self.name}"

    def getReplenish(self):
        if self.optimal_stock:
            return self.optimal_stock - self.real_quantity
        return 0

    def getUom(self):
        return self.uom

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


class Inventory(models.Model):
    name = models.CharField(_("name"), max_length=80)
    isApply = models.BooleanField(_("est appliqué"), default=False)
    date = models.DateField(_("date"))

    created_by = models.ForeignKey(
        NewUser, related_name="created_inventories", on_delete=models.CASCADE
    )
    modified_by = models.ForeignKey(
        NewUser, related_name="modified_inventories", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "inventory"
        verbose_name_plural = "inventories"

    def __str__(self):
        return format(self.name)


class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        related_name="items_inventory",
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Product,
        related_name="items_product",
        on_delete=models.CASCADE,
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
