from django.db import models
from django.db.models import Avg
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
    use_for_bi = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    comments = models.ManyToManyField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def number_of_columns(self):
        return self.columns.count()

    @property
    def average_percentage_of_nulls(self):
        return self.columns.aggregate(
            average_percentage_of_nulls=Avg("percentage_of_nulls")).\
            get("average_percentage_of_nulls")

    @property
    def columns_needing_indexes(self):
        return self.columns.filter(needs_index=True)


class Column(TimeStampedModel):

    class Meta:
        ordering = ['name']

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
        verbose_name=_('Number of null values'))
    percentage_of_nulls = models.DecimalField(
        max_digits=11, decimal_places=2, null=True, db_index=True,
        verbose_name=_('Percentage of null values'))
    unique_values = models.IntegerField(
        blank=True, null=True, db_index=True,
        verbose_name=_('Number of unique values'))
    has_duplicates = models.NullBooleanField(
        verbose_name=_('Does the column contain duplicates'),
        db_index=True)
    is_structured = models.NullBooleanField(
        verbose_name=_('Is well structured'),
        db_index=True)
    needs_index = models.NullBooleanField(
        verbose_name=_('Needs index'),
        db_index=True)
    comments = models.ManyToManyField("Comment", blank=True, null=True)

    def __str__(self):
        return self.name


class ValueDistribution(TimeStampedModel):

    class Meta:
        ordering = ["value"]

    column = models.ForeignKey(
        "Column", related_name="value_distributions",
        on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Value: {}, Count: {}".format(self.value, self.count)


class ColumnStatistics(TimeStampedModel):

    column = models.OneToOneField(
        'Column', related_name='statistics', on_delete=models.CASCADE)

class Comment(TimeStampedModel):

    text = models.TextField(blank=True)
