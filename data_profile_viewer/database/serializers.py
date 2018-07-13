from rest_framework import serializers

from database.models import Table, Column

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "schema", "number_of_rows"]
        model = Table


class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = [
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
            "has_duplicates"
        ]
