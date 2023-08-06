from __future__ import unicode_literals

import json

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.shortcuts import render
from reviewboard.admin.server import build_server_url
from reviewboard.site.urlresolvers import local_site_reverse


def manifest(request, config_hash):
    return HttpResponse(
        json.dumps({
            'name': 'Review Board',
            'details': 'Links Trello tasks to review requests on Review Board.',
            'icon': {
                'url': build_server_url(static('rb/images/logo.png')),
            },
            'author': 'Beanbag, Inc.',
            'capabilities': [
                'authorization-status',
                'attachment-sections',
                'attachment-thumbnail',
                'board-buttons',
                'callback',
                'card-badges',
                'card-buttons',
                'card-detail-badges',
                'card-from-url',
                'format-url',
                'show-authorization',
                'show-settings',
            ],
            'connectors': {
                'iframe': {
                    'url': build_server_url(local_site_reverse(
                        'trello-index',
                        kwargs={
                            'config_hash': config_hash,
                        },
                        request=request)),
                },
            },
        }),
        content_type='application/json')


def index(request, config_hash):
    from rbintegrations.extension import RBIntegrationsExtension

    return render(request, 'trello/index.html', {
        'extension': RBIntegrationsExtension.instance,
    })
