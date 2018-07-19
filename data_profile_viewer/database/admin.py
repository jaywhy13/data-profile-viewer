from django.contrib import admin

from database.models import Table, Column, ColumnStatistics, ValueDistribution

admin.site.register(Table)
admin.site.register(Column)
admin.site.register(ValueDistribution)

admin.site.register(ColumnStatistics)
