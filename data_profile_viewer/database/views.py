from django.views.generic import TemplateView

from database.models import Column


class SQLIndexesView(TemplateView):

    template_name = "database/indexes.html"
    context_type = "text/richtext"

    def get_context_data(self, **kwargs):
        ctx =super(SQLIndexesView, self).get_context_data(**kwargs)
        columns = Column.objects.filter(needs_index=True)
        ctx["columns"] = columns
        return ctx
