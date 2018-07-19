from rest_framework import viewsets

from database.models import Table, Column
from database.serializers import TableSerializer, ColumnSerializer


class TableViewSet(viewsets.ModelViewSet):

    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ColumnViewSet(viewsets.ModelViewSet):

    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

    @action(methods=['post'], detail=True)
    def update_has_duplicates(self, request, pk=None):
        column = self.get_object()
        has_duplicates = request.data.get("has_duplicates")
        column.has_duplicates = has_duplicates
        column.save()
        serializer = ColumnSerializer(column, many=False)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_is_structured(self, request, pk=None):
        column = self.get_object()
        is_structured = request.data.get("is_structured")
        column.is_structured = is_structured
        column.save()
        serializer = ColumnSerializer(column, many=False)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_needs_index(self, request, pk=None):
        column = self.get_object()
        needs_index = request.data.get("needs_index")
        column.needs_index = needs_index
        column.save()
        serializer = ColumnSerializer(column, many=False)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def value_distributions(self, request, pk=None):
        column = self.get_object()
        value_distributions = column.value_distributions.all()
        page = self.paginate_queryset(value_distributions)
        if page is not None:
            serializer = ValueDistributionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ValueDistributionSerializer(
            value_distributions, many=True)
        return Response(serializer.data)

