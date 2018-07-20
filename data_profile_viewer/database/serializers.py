from rest_framework import serializers

from database.models import Table, Column, ValueDistribution

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "name", "schema", "number_of_rows",
            "number_of_columns", "average_percentage_of_nulls",
            "use_for_bi"]
        model = Table
        lookup_field = 'name'


class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = [
            "id",
            "table",
            "name",
            "data_type",
            "max_length",
            "minimum",
            "maximum",
            "standard_deviation",
            "max_length",
            "is_null",
            "null_count",
            "unique_values",
            "has_duplicates",
            "percentage_of_nulls",
            "is_structured",
            "needs_index",
        ]

class ValueDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["value", "count"]
        model = ValueDistribution
