# coding=utf-8
"""
Defines a few (slightly silly) Django models that we can use in unit
tests.
"""

from __future__ import absolute_import, division, print_function, \
  unicode_literals

from django.db import models


class Specie(models.Model):
    common_name =\
      models.CharField(
        db_index    = True,
        max_length  = 40,
        unique      = True,
      )

    binomial_name =\
      models.CharField(
        db_index    = True,
        max_length  = 40,
        unique      = True,
      )

    is_cuddly =\
      models.NullBooleanField()

    last_sighted =\
      models.DateTimeField(
        null = True,
      )

    color =\
      models.CharField(
        max_length  = 24,
        default     = 'green',
      )
