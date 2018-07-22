from pprint import pprint
import os
import untangle

import logging
from django.core.management.base import BaseCommand

from database.models import Table, Column, ValueDistribution

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import data from an SQL Data Profile Viewer XML file"

    created_tables = {}
    column_cache = {}
    table_cache = {}

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):
        file = options.get("file")[0]
        self.xml_obj = self.parse_xml_profile_data(file=file)
        column_profiles = self.get_column_profiles()
        for column_profile in column_profiles:
            self.save_tables_and_columns(column_profile)
        self._save_cached_tables_and_columns()

    def parse_xml_profile_data(self, file=None):
        """ Reads in the XML profile data
        """
        if not os.path.exists(file):
            raise Exception("The file {} does not exist".format(file))
        print("Reading in {}".format(file))
        xml_obj = untangle.parse(file)
        print("Done reading")
        return xml_obj

    def get_column_profiles(self):
        """ Returns the profile data (null ratio profile and stats)
        """
        profiles = self.xml_obj.DataProfile.DataProfileOutput.Profiles
        for profile in profiles.ColumnNullRatioProfile:
            yield profile
        for profile in profiles.ColumnStatisticsProfile:
            yield profile
        for profile in profiles.ColumnValueDistributionProfile:
            yield profile
        for profile in profiles.ColumnLengthDistributionProfile:
            yield profile

    def save_tables_and_columns(self, column_profile):
        self._cache_tables_and_columns(column_profile)
        if self._is_cache_full():
            self._save_cached_tables_and_columns()

    def _is_cache_full(self):
        return len(self.column_cache) > 200

    def _cache_tables_and_columns(self, column_profile):
        table_name = \
            self.get_table_name(column_profile)
        table_data = self.table_cache.setdefault(table_name, {})
        table_data["name"] = table_name
        table_data["number_of_rows"] = \
            int(column_profile.Table["RowCount"])
        table_data["schema"] = self.get_table_schema(column_profile)
        column_name = \
            self.get_column_name(table_name, column_profile)
        if not column_name:
            raise Exception("There is a column here on {} that has NO name".format(table_name))
        # print("Caching {}.{}".format(table_name, column_name))
        column_key = self._build_column_key(table_name, column_name)
        column_data = self.column_cache.setdefault(column_key, {})
        column_data["name"] = column_name
        column_data["table_name"] = table_name
        column_data["data_type"] = column_profile.Column["SqlDbType"]
        if column_profile.Column["IsNullable"]:
            column_data["is_null"] = True if column_profile.Column["IsNullable"] == 'true' else False
        if column_profile.Column["MaxLength"]:
            column_data["max_length"] = column_profile.Column["MaxLength"]
        if hasattr(column_profile, "NullCount"):
            column_data["null_count"] = float(column_profile.NullCount.cdata)
        if hasattr(column_profile, "MinValue"):
            column_data["minimum"] = column_profile.MinValue.cdata
        if hasattr(column_profile, "MaxValue"):
            column_data["maximum"] = column_profile.MaxValue.cdata
        if hasattr(column_profile, "StdDev"):
            column_data["standard_deviation"] = column_profile.StdDev.cdata
        if hasattr(column_profile, "NumberOfDistinctValues"):
            column_data["unique_values"] = \
                column_profile.NumberOfDistinctValues.cdata or 0
        if hasattr(column_profile, "ValueDistribution"):
            values_and_counts = \
                column_profile.ValueDistribution.ValueDistributionItem
            value_distributions = \
                column_data.setdefault("value_distributions", [])
            for value_distribution_item in values_and_counts:
                value = value_distribution_item.Value.cdata
                count = value_distribution_item.Count.cdata or 0
                value_distributions.append((value, count))
        # pprint(column_data)

    def _save_cached_tables_and_columns(self):
        print("> Saving {} tables and {} columns".format(
            len(self.table_cache), len(self.column_cache)))
        for table_name in self.table_cache:
            table_data = self.table_cache.get(table_name)
            table, _ = \
                Table.objects.update_or_create(name=table_name,
                                               defaults=table_data)
            self.created_tables[table_name] = table
        for column_key in self.column_cache:
            _, column_name = self._extract_column_key(column_key)
            column_data = self.column_cache.get(column_key)
            table_name = column_data.get("table_name")
            # print("Saving {}.{}".format(table_name, column_data))
            # pprint(column_data)
            value_distributions = column_data.pop("value_distributions", [])
            table = self.created_tables.get(table_name)
            if not table:
                raise Exception("Could not find table: {} for {}".format(
                    table_name, column_name))
            defaults = {
                "name": column_data.get("name"),
                "data_type": column_data.get("data_type"),
                "is_null": column_data.get("is_null"),
                "max_length": column_data.get("max_length"),
                "table": table,
            }
            other_attributes = [
                "minimum",
                "maximum",
                "standard_deviation",
                "null_count",
                "unique_values"
            ]
            for other_attribute in other_attributes:
                if other_attribute in column_data:
                    defaults[other_attribute] = \
                        column_data.get(other_attribute)
            # Update the null ratio based on the table
            if table.number_of_rows > 0 and "null_count" in column_data:
                defaults["percentage_of_nulls"] = \
                    column_data["null_count"] / table.number_of_rows
            column, _ = Column.objects.update_or_create(table=table,
                                                        name=column_name,
                                                        defaults=defaults)
            # Saving value distributions
            for value, count in value_distributions:
                defaults = {
                    "count": count
                }
                ValueDistribution.objects.update_or_create(column=column,
                                                           value=value,
                                                           defaults=defaults)
        self.column_cache = {}
        self.table_cache = {}


    def get_table_name(self, column_profile):
        table_name = column_profile.Table["Table"]
        return table_name

    def get_table_schema(self, column_profile):
        schema = column_profile.Table["Schema"]
        return schema

    def get_column_name(self, table_name, column_profile):
        column_name = column_profile.Column["Name"]
        return column_name

    def _build_column_key(self, table_name, column_name):
        return "{}--{}".format(table_name, column_name)

    def _extract_column_key(self, column_key):
        return column_key.split("--")


