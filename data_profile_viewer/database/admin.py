from django.contrib import admin

from database.models import Table, Column, ColumnStatistics

admin.site.register(Table)
admin.site.register(Column)

admin.site.register(ColumnStatistics)
