# -*- coding: utf-8 -*-
"""
Formularios para la app globales
"""
# Standard Library
import re

from apps.account.models import NewUser
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _


class PersonaChangeForm(UserChangeForm):
    """For something it will be this
    """
    class Meta(UserChangeForm.Meta):
        model = NewUser
        fields = (
            'email',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            # 'date_joined',
            'first_name',
            'last_name',
        )


# ========================================================================== #

class PersonaCreationForm(UserCreationForm):
    """With this form class, the registration template is rendered.
    users
    """
    class Meta(UserCreationForm.Meta):
        model = NewUser
        fields = (
            'email',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': _('Email')}
            ),
        }


    """To activate or deactivate an object in Gomag
    """
    object_name = forms.CharField(max_length=100, widget=forms.HiddenInput)
    object_pk = forms.IntegerField(widget=forms.HiddenInput)
