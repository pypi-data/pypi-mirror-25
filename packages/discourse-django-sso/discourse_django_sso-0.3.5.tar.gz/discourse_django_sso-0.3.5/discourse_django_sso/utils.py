# coding=utf-8

"""Actual implementation of SSO"""


import base64
import enum
import hashlib
import hmac
import typing
from urllib.parse import parse_qs, urlencode

import logging
from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.encoding import force_bytes

SSOResponse = typing.NamedTuple(
    "SSOResponse",
    (
        ("noonce", bytes),
        ("redirect", str)
    )
)


SignedPayload = typing.NamedTuple(
    "SignedPayload",
    (
        ("sso", bytes),
        ("sig", bytes)
    )
)


class ConsumerType(enum.Enum):
    """
    Enum representing whether a costumer is a Discourse instance
    or something else.
    """

    DISCOURSE = "discourse"
    OTHER = "other"


class BaseSSOGenerator(object):

    """Base class for SSO generator."""

    def __init__(self, sso_key: typing.Union[str, bytes]):
        self.sso_key = force_bytes(sso_key)

    def _get_payload_singature(self, payload: typing.Union[str, bytes]) -> bytes:
        """Returns HMAC signature for ``payload``."""
        digest = hmac.new(self.sso_key, force_bytes(payload), digestmod=hashlib.sha256).hexdigest()
        return force_bytes(digest)

    def prepare_signed_payload(
            self,
            params: typing.Union[dict, typing.Sequence[typing.Tuple[str, str]]]
    ) -> SignedPayload:
        """Prepare payload and signature."""
        encoded_params = base64.b64encode(force_bytes(urlencode(params)))
        response_sig = self._get_payload_singature(encoded_params)
        return (
            ('sso', encoded_params),
            ('sig', response_sig),
        )

    def _verify_payload(
            self,
            payload: typing.Union[str, bytes],
            signature: typing.Union[str, bytes]
    ) -> bool:
        """Verifies that signature is correct for payload."""
        this_signature = self._get_payload_singature(payload)
        result = constant_time_compare(
            this_signature,
            force_bytes(signature)
        )
        return result


class SSOProducerUtils(BaseSSOGenerator):
    """Utils for SSO producer."""

    def __init__(
            self,
            sso_key: typing.Union[str, bytes],
            consumer_url: str,
            user: settings.AUTH_USER_MODEL,
            sso: typing.Union[str, bytes],
            sig: typing.Union[str, bytes]
    ):
        """
        Init function, gets unpacked parameters from SSO endpoint,
        as well as logged in user.
        """
        super().__init__(sso_key)
        self.consumer_url = consumer_url
        assert isinstance(self.consumer_url, str)
        self.user = user
        self.sso = force_bytes(sso)
        self.sig = force_bytes(sig)

    def validate(
            self,
            consumer_type: ConsumerType = ConsumerType.DISCOURSE
    ):
        """Validate this sso instance, this should perform sanity checks."""
        if consumer_type == ConsumerType.DISCOURSE:
            # Discourse produces SSO that ends with a new line
            # it you accidentally trim it you'll get invalid key,
            # and will not have a good time debugging it.
            if self.sso[-1:] != b'\n':
                raise ValueError(
                    "Invalid sso. SSO should end with new line, "
                    "(discourse generates sso string ending with "
                    "'\\n')."
                    "SSO IS: '{}'".format(self.sso)
                )

        payload = base64.b64decode(self.sso)
        if b'nonce' not in payload:
            raise ValueError(self.sso, payload)

    @property
    def request_payload(self) -> str:
        """Returns decoded request payload."""
        payload = base64.b64decode(self.sso)
        return payload

    def verify_signature(self) -> bool:
        """Verifies the signature."""
        return self._verify_payload(self.sso, self.sig)

    def get_nonce(self) -> bytes:
        """Returns nonce from request payload."""
        parsed_payload = parse_qs(self.request_payload)
        return parsed_payload[b'nonce'][0]

    def get_response_params(self) -> typing.Sequence[typing.Tuple[str, str]]:
        """
        Returns SSO response parameters.

        Tuple of tuples is returned instead of a dict to have
        deterministic ordering of parameters, as order of parameters
        changes signature, and makes testing harder.
        """
        return (
            ('nonce', self.get_nonce()),
            ('email', self.user.email),
            ('username', self.user.username),
            ('external_id', self.user.id),
        )

    def get_signed_payload(self) -> dict:
        """Returns signed GET parameters for redirect."""
        return self.prepare_signed_payload(self.get_response_params())

    def get_sso_redirect(self, signed_payload) -> str:
        """Get full sso redirect."""
        query_string = urlencode(signed_payload)
        return '%s?%s' % (self.consumer_url, query_string)


class SSOProviderService(object):
    """
    SSO provider service.
    """

    def __init__(self, sso_key):
        """
        :param sso_key: SSO shared secret key.
        """
        self.sso_key = sso_key

    def get_signed_url(
            self,
            user: settings.AUTH_USER_MODEL,
            sso: str,
            signature: str,
            redirect_to: str,
            consumer_type: ConsumerType = ConsumerType.DISCOURSE
    ) -> typing.Optional[str]:
        """
        Performs SSO, returning redirect url.

        :param user: User that will be logged in using SSO.
        :param sso: SSO string received from consumer
        :param signature: Signature for sso string
        :param redirect_to: Endpoint user will be redirected to
        :param consumer_type: type of SSO consumer, can be used to
                              customize SSO a bit.
        """

        gen = SSOProducerUtils(
            sso_key=self.sso_key,
            consumer_url=redirect_to,
            user=user,
            sso=sso,
            sig=signature
        )
        try:
            gen.validate(consumer_type=consumer_type)
        except ValueError:
            logging.exception("Invalid sso")
            return None
        if not gen.verify_signature():
            return None
        payload = gen.get_signed_payload()
        return gen.get_sso_redirect(payload)


