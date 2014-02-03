"""
Annalist action confirmation view definition
"""

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2014, G. Klyne"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import os.path
import json
import random
import logging
import uuid
import copy

import logging
log = logging.getLogger(__name__)

# import rdflib
# import httplib2

from django.http                    import HttpResponse
from django.http                    import HttpResponseRedirect
from django.http                    import QueryDict
from django.template                import RequestContext, loader
from django.core.urlresolvers       import resolve, reverse

from django.conf                    import settings

from annalist.views                 import AnnalistGenericView

def querydict_dict(querydict):
    """
    Converts a Django QueryDict value to a regular dictionary, preserving multiple items.
    """
    return dict(querydict.iterlists())

def dict_querydict(dict_):
    """
    Converts a value created by querydict_dict back into a Django QueryDict value.
    """
    q = QueryDict("", mutable=True)
    for k, v in dict_.iteritems():
        q.setlist(k, v)
    q._mutable = False
    return q

def querydict_dumps(querydict):
    """
    Converts a Django QueryDict value to a serialized form, preserving multiple items.

    Serializes as JSON where each key has a list value.
    """
    return json.dumps(querydict_dict(querydict))

def querydict_loads(querydict_s):
    """
    Converts a serialized Django QueryDict back to its internal value.
    """
    return dict_querydict(json.loads(querydict_s))

class ConfirmView(AnnalistGenericView):
    """
    View class to handle response to request to confirm action
    """
    def __init__(self):
        super(ConfirmView, self).__init__()
        return

    @staticmethod
    def render_form(request,
            action_description="(description of action to perform)",
            action_params={},
            complete_action='(name of "urls" pattern to dispatch to complete action)',
            cancel_action='(name of "urls" pattern to dispatch to cancel action)',
            title=None):
        """
        Render form that requests a user to confirm an action to be performed and,
        depending onthe user's response, redirects tp 'complete_action' or 
        """
        form_data = (
            { "action_description":     action_description
            , "action_params":          querydict_dumps(action_params)
            , "complete_action":        reverse(complete_action)
            , "cancel_action":          reverse(cancel_action)
            , "title":                  title
            , "suppress_user":          True
            })
        template = loader.get_template('annalist_confirm.html')
        context  = RequestContext(request, form_data)
        log.info("confirmview form data: %r"%(form_data))
        return HttpResponse(template.render(context))

    # POST

    def post(self, request):
        """
        Handle POST of form data soliciting user confirmation of action.

        Creates a new request object with the original action POST data, and dispatches
        to the appropriate completion view function.  This function should, in turn,
        return a redirect to an appripriate continuation display.

        If the operation is canceled, then this function returns an HTTP redirect to 
        the "cancel_action" continuation URI.
        """
        log.info("confirmview.post: %r"%(request.POST))
        params         = querydict_loads(request.POST["action_params"])
        action_request = copy.copy(request)
        if request.POST.get("confirm", None):
            view, args, kwargs  = resolve(request.POST["complete_action"])
            action_request.POST = params
            return view(action_request)
        return HttpResponseRedirect(request.POST["cancel_action"])

# End.
