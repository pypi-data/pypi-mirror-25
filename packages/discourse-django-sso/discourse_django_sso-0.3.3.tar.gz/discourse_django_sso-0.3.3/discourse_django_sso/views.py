"""Views module"""

import uuid
from abc import ABC, abstractmethod

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


class NonceService(ABC):
    """
    Service for managing nonce.
    """

    @abstractmethod
    def generate_nonce(self):
        pass

    @abstractmethod
    def is_nonce_valid(self, nonce: str):
        pass

    @abstractmethod
    def invalidate_nonce(self, nonce: str):
        pass


class InMemoryNonceService(NonceService):
    """
    In memory implementation of nonce service
    """

    def __init__(self):
        self.generated_nonces = set()
        self.invalid_nonces = set()

    def generate_nonce(self) -> str:
        #TODO For generating secure noonces we could use: https://docs.python.org/3.4/library/random.html#random.SystemRandom
        val = uuid.uuid4().hex
        while val in self.generated_nonces:
            val = uuid.uuid4().hex      # pragma: no cover
        self.generated_nonces.add(val)
        return val

    def is_nonce_valid(self, nonce: str) -> bool:
        return nonce in self.generated_nonces and nonce not in self.invalid_nonces

    def invalidate_nonce(self, nonce: str):
        self.invalid_nonces.add(nonce)


class SSOClientView(LoginRequiredMixin, View):
    """
    View for the client of the sso
    """

    def __init__(self, sso_secret: str, sso_url: str, nonce_service: NonceService):
        self.nonce_service = nonce_service
        self.client_util = utils.SSOClientUtils(sso_secret, sso_url)

    def get(self, request, **kwargs):  # pylint: disable=unused-argument
        #TODO how do we know about email value - true/false
        sso_url = self.client_util.generate_sso_url(self.nonce_service.generate_nonce(), False)

        return HttpResponseRedirect(
            redirect_to=sso_url
        )


class SSOCreateSessionView(LoginRequiredMixin, View):
    """
    View for processing of response from sso provider
    """

    def __init__(self, sso_secret: str, nonce_service: NonceService):
        self.sso_secret = sso_secret
        self.nonce_service = nonce_service
        self.client_util = utils.SSOClientUtils(sso_secret, None)

    def get(self, request, **kwargs):  # pylint: disable=unused-argument
        """Performs the session creation"""
        try:
            sso = request.GET['sso']
            sig = request.GET['sig']
        except KeyError:
            return HttpResponseBadRequest()
        if not self.client_util.validate_sso_against_sid(sso, sig):
            return HttpResponseBadRequest()
        user_data = self.client_util.decode_client_data(sso)
        nonce = self.client_util.get_param(user_data, b'nonce')
        if self.nonce_service.is_nonce_valid(nonce):
            self.create_user_session(self.client_util.get_param(b'email'), self.client_util.get_param(b'external_id'),
                                     self.client_util.get_param(b'username'))
            self.nonce_service.invalidate_nonce(nonce)
        else:
            return HttpResponseBadRequest()

    def create_user_session(self, user_email, external_id, username):
        #TODO ??
        pass
