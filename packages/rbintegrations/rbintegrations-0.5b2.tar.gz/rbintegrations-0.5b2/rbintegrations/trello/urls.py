from __future__ import unicode_literals

from django.conf.urls import include, url

from rbintegrations.trello.views import manifest, index


urlpatterns = [
    url('^trello/(?P<config_hash>[A-Za-z0-9]+)/', include([
        url('^manifest.json$', manifest, name='trello-manifest'),
        url('^index/$', index, name='trello-index'),
    ])),
]
