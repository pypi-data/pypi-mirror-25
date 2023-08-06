# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic.base import TemplateView

from soft_drf.doc.api_docs import ApiDocumentation
from soft_drf.routing.v1.routers import router


class DRFDocsView(TemplateView):

    template_name = "api_documentation.html"
    drf_router = router

    def get_context_data(self, **kwargs):
        context = super(DRFDocsView, self).get_context_data(**kwargs)
        docs = ApiDocumentation(drf_router=self.drf_router)
        endpoints = docs.get_endpoints()
        title = "TITLE PROJECT BASE"

        if hasattr(settings, 'TITLE_DOCUMENTATION'):
            title = settings.TITLE_DOCUMENTATION

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [
                endpoint for endpoint in endpoints if query in endpoint.path
            ]

        context['title'] = title
        context['query'] = query
        context['endpoints'] = endpoints
        return context
