from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.forms.fields import ConditionsField
from reviewboard.integrations.forms import IntegrationConfigForm
from reviewboard.reviews.conditions import ReviewRequestConditionChoices


class TrelloIntegrationConfigForm(IntegrationConfigForm):
    """Form for configuring Trello.

    This allows an administrator to set up a Trello configuration for
    providing details of review requests on Trello cards/boards, and for
    linking review requests to tasks.
    """

