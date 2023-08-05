# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db.models import Model
from django.utils.encoding import force_text
from django.utils.six import python_2_unicode_compatible
from templateselector.fields import TemplateField

@python_2_unicode_compatible
class MyModel(Model):
    f = TemplateField(match="^admin/.+\.html$", verbose_name="test 'f'")

    def __str__(self):
        return force_text(self.pk)
