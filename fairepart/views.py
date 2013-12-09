from __future__ import unicode_literals

import logging

from django.views import generic
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .backends import get_backends
from .models import Relation

from . import settings

logger = logging.getLogger('fairepart')


class ImportView(generic.View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        backend_name = self.kwargs.get('backend')

        backends = get_backends()

        if backend_name not in backends:
            return HttpResponseBadRequest('%s backend not found' % backend_name)

        backend_class = backends.get(backend_name)

        backend = backend_class()
        backend.import_from_user(request.user)

        return HttpResponseRedirect(reverse('fairepart_relation_list', args=[backend_name, ]))


class RelationListView(generic.ListView):
    model = Relation
    template_name = 'fairepart/relation_list.html'
    paginate_by = settings.RELATION_LIST_PAGINATE_BY

    def get_queryset(self):
        qs = super(RelationListView, self).get_queryset().filter(from_user=self.request.user)

        self.provider = self.kwargs.get('provider', None)

        if self.provider:
            qs = qs.filter(provider=self.provider)

        return qs

    def get_context_data(self, **kwargs):
        context = super(RelationListView, self).get_context_data(**kwargs)
        context['provider'] = self.provider

        return context

    def get_template_names(self):
        template_names = [self.template_name, ]

        if self.provider:
            template_names = [
                'fairepart/%s_relation_list.html' % self.provider,
            ] + template_names

        return template_names
