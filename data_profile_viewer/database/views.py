from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from database.models import Column, Table


class SQLIndexesView(LoginRequiredMixin, TemplateView):

    template_name = "database/indexes.html"
    context_type = "text/richtext"

    def get_context_data(self, **kwargs):
        ctx =super(SQLIndexesView, self).get_context_data(**kwargs)
        tables = Table.objects.all()
        ctx["tables"] = tables
        return ctx


class SQLTruncateView(LoginRequiredMixin, TemplateView):

    template_name = "database/truncate.html"
    context_type = "text/richtext"

    def get_context_data(self, **kwargs):
        ctx =super(SQLTruncateView, self).get_context_data(**kwargs)
        tables = Table.objects.filter()
        ctx["tables"] = tables
        return ctx
