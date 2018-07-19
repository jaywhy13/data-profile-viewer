from django.db import models
from django.utils.translation import gettext as _

from django_extensions.db.models import TimeStampedModel


class Table(TimeStampedModel):

    class Meta:
        ordering = ['name']

    name = models.CharField(
        max_length=255, blank=True, null=True, db_index=True)
    schema = models.CharField(
        max_length=255, blank=True, null=True, db_index=True)
    number_of_rows = models.IntegerField(
        blank=True, null=True, db_index=True)

    def __str__(self):
        return self.name


class Column(TimeStampedModel):

    table = models.ForeignKey(
        Table, db_index=True, null=True, blank=True,
        related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255, blank=True, null=True, db_index=True)
    data_type = models.CharField(max_length=255, db_index=True)
    minimum = models.TextField(blank=True, null=True)
    maximum = models.TextField(blank=True, null=True)
    standard_deviation = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    is_null = models.NullBooleanField()
    null_count = models.DecimalField(
        max_digits=11, decimal_places=2, null=True, db_index=True,
        verbose_name=_('Percentage of nulls'))
    unique_values = models.IntegerField(
        blank=True, null=True, db_index=True,
        verbose_name=_('Number of unique values'))
    has_duplicates = models.NullBooleanField(
        verbose_name=_('Does the column contain duplicates'),
        db_index=True)

    def __str__(self):
        return self.name


class ColumnStatistics(TimeStampedModel):

    column = models.OneToOneField(
        'Column', related_name='statistics', on_delete=models.CASCADE)

class Comment(TimeStampedModel):

    text = models.TextField(blank=True)
