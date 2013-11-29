from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns(
    '',

    url(r'^import/(?P<backend>[^/]+)/$',
        login_required(views.ImportView.as_view()),
        name='fairepart_import'),

    url(r'^relations/(?P<provider>[^/]+)/(?:(?P<page>[\d]+)/)?$',
        login_required(views.RelationListView.as_view()),
        name='fairepart_relation_list'),
)
