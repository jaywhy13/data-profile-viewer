from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


from database.models import Table, Column, ValueDistribution
from database.serializers import (
    TableSerializer,
    ColumnSerializer,
    ValueDistributionSerializer
)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TableViewSet(viewsets.ModelViewSet):

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'name'
    authentication_classes = (
        BasicAuthentication, CsrfExemptSessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(TableViewSet, self).get_queryset()
        query = self.request.query_params.get("q", None)
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    @action(detail=True)
    def columns(self, request, name=None):
        table = self.get_object()
        columns = table.columns.all()
        column_query = request.query_params.get("cq", None)
        if column_query:
            columns = columns.filter(name__icontains=column_query)
        page = self.paginate_queryset(columns)
        if page is not None:
            serializer = ColumnSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_use_for_bi(self, request, name=None):
        table = self.get_object()
        use_for_bi = request.data.get("use_for_bi")
        table.use_for_bi = use_for_bi
        table.save()
        serializer = TableSerializer(table, many=False)
        return Response(serializer.data)


class ColumnViewSet(viewsets.ModelViewSet):

    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    authentication_classes = (
        BasicAuthentication, CsrfExemptSessionAuthentication)
    permission_classes = (IsAuthenticated,)

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


class ValueDistributionViewSet(viewsets.ModelViewSet):

    queryset = ValueDistribution.objects.all()
    serializer_class = ValueDistributionSerializer

