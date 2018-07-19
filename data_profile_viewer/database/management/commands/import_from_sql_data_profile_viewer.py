from pprint import pprint
import os
import untangle

import logging
from django.core.management.base import BaseCommand

from database.models import Table, Column, ValueDistribution

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import data from an SQL Data Profile Viewer XML file"

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
        if self._is_cache_full():
            self._save_cached_tables_and_columns()
        self._cache_tables_and_columns(column_profile)

    def _is_cache_full(self):
        return len(self.column_cache) > 100

    def _cache_tables_and_columns(self, column_profile):
        table_name = \
            self.get_table_name(column_profile)
        table_data = self.table_cache.setdefault(table_name, {})
        table_data["name"] = table_name
        table_data["number_of_rows"] = \
            int(column_profile.Table["RowCount"])
        table_data["schema"] = self.get_table_schema(column_profile)
        column_name, column_data = \
            self.get_column_name_and_data(table_name, column_profile)
        column_data = self.column_cache.setdefault(column_name, {})
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

    def _save_cached_tables_and_columns(self):
        print("Saving column profile cache")
        created_tables = {}
        for table_name in self.table_cache:
            table_data = self.table_cache.get(table_name)
            table, _ = \
                Table.objects.update_or_create(name=table_name,
                                               defaults=table_data)
            created_tables[table_name] = table
        for column_name in self.column_cache:
            column_data = self.column_cache.get(column_name)
            value_distributions = column_data.pop("value_distributions", [])
            table_name = column_data.get("table_name")
            table = created_tables.get(table_name)
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

            print("Updating column {}".format(column_name))
            pprint(defaults)
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

    def get_column_name_and_data(self, table_name, column_profile):
        column_name = column_profile.Column["Name"]
        column_data = {}
        return column_name, column_data


