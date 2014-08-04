from __future__ import unicode_literals

import logging

from django.views import generic
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from .backends import get_backends
from .models import Relation
from .forms import InvitationForm

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
    context_object_name = 'relation_list'

    def get_queryset(self):
        qs = super(RelationListView, self).get_queryset().filter(from_user=self.request.user)

        self.provider = self.kwargs.get('provider', None)

        if self.provider:
            qs = qs.filter(provider=self.provider)

        query = self.request.GET.get('q', None)

        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(name__istartswith=query))

        return qs

    def get_context_data(self, **kwargs):
        context = super(RelationListView, self).get_context_data(**kwargs)
        context['provider'] = self.provider
        context['from_user'] = self.request.user

        for relation in context[self.context_object_name]:
            relation.from_user = self.request.user

        return context

    def get_template_names(self):
        template_names = [self.template_name, ]

        if self.provider:
            template_names = [
                'fairepart/%s_relation_list.html' % self.provider,
            ] + template_names

        return template_names


class InviteView(generic.CreateView):
    form_class = InvitationForm
    template_name = 'fairepart/invite.html'

    def get_form_kwargs(self):
        kwargs = super(InviteView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        if self.request.is_ajax():
            return HttpResponse('Ok', status=201)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('fairepart_invite_done')


class InviteDoneView(generic.TemplateView):
    template_name = 'fairepart/invite_done.html'
