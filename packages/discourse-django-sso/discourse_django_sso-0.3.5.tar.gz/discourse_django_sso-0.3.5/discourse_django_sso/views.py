"""Views module"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import View

from discourse_django_sso import utils
from discourse_django_sso.utils import ConsumerType


class SSOProviderView(LoginRequiredMixin, View):
    """
    View that implements sso.
    """

    sso_secret = None
    sso_redirect = None
    consumer_type = ConsumerType.DISCOURSE

    def get(self, request, **kwargs):  # pylint: disable=unused-argument
        """Performs the SSO"""
        try:
            sso = request.GET['sso']
            sig = request.GET['sig']
        except KeyError:
            return HttpResponseBadRequest()
        redirect = utils.SSOProviderService(
            sso_key=self.sso_secret
        ).get_signed_url(
            user=request.user,
            redirect_to=self.sso_redirect,
            sso=sso,
            signature=sig,
            consumer_type=self.consumer_type
        )
        if redirect is None:
            return HttpResponseBadRequest()
        return HttpResponseRedirect(
            redirect_to=redirect
        )


