from django.contrib import admin

from database.models import Table, Column, ColumnStatistics, ValueDistribution

admin.site.register(Table)
admin.site.register(ValueDistribution)

admin.site.register(ColumnStatistics)


class PercentageFilter(admin.SimpleListFilter):

    title = 'Percentage of nulls'

    parameter_name = 'null_ratio'

    def lookups(self, request, model_admin):
        return [
            ('', 'Unknown'),
            ('25', 'Up to 25%'),
            ('50', 'Up to 50%'),
            ('75', 'Up to 75%'),
            ('100', 'Up to 100%'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '':
            return queryset.filter(percentage_of_nulls=None)
        elif self.value() == '25':
            return queryset.filter(percentage_of_nulls__lte=0.25)
        elif self.value() == '50':
            return queryset.filter(percentage_of_nulls__lte=0.5)
        elif self.value() == '75':
            return queryset.filter(percentage_of_nulls__lte=0.75)
        return queryset


class ColumnAdmin(admin.ModelAdmin):

    ordering = [
        "table__name",
        "name"
    ]

    list_select_related = ["table"]

    list_display = [
        "table_name", "name", "data_type",
        "minimum", "maximum", "standard_deviation",
        "max_length", "is_null", "percentage_of_nulls",
        "unique_values", "is_structured", "needs_index"]

    list_filter = [
        "is_null",
        "is_structured",
        PercentageFilter,
        "needs_index",
        "table__use_for_bi",
        "table__name",
    ]

    search_fields = [
        "name",
        "table__name"
    ]

    def table_name(self, obj):
        return obj.table.name

admin.site.register(Column, ColumnAdmin)
