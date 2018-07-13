from rest_framework import viewsets

from database.models import Table, Column
from database.serializers import TableSerializer, ColumnSerializer


class TableViewSet(viewsets.ModelViewSet):

    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ColumnViewSet(viewsets.ModelViewSet):

    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
