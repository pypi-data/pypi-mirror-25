# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from _datetime import datetime


class SpitzerMigrationsModel(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    migration = models.CharField(max_length=300)
    checksum = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=datetime.now())
    executed = models.IntegerField(blank=True, null=True)
    success = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spitzer_migrations'
