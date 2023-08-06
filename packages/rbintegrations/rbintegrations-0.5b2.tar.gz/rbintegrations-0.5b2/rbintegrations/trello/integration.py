from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from reviewboard.extensions.hooks import URLHook
from reviewboard.integrations import Integration

from rbintegrations.trello.forms import TrelloIntegrationConfigForm
from rbintegrations.trello.urls import urlpatterns


class TrelloIntegration(Integration):
    name = 'Trello'
    description = _(
        'Enables usage of the Review Board Power Up for Trello boards '
        'and integrates review requests with Trello tasks.'
    )

    default_settings = {
        'config_hash': '',
    }

    config_form_cls = TrelloIntegrationConfigForm

    def initialize(self):
        """Initialize the integration."""
