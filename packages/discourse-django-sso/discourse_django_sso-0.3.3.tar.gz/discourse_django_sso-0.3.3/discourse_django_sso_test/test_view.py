# coding=utf-8

"""Test sso view."""

import base64
import hashlib
import hmac
from urllib.parse import urlencode

import pytest
from django.test.client import Client
from django.urls.base import reverse
from django.utils.encoding import force_bytes

from discourse_django_sso_test_project import settings


# pylint: disable=missing-docstring,redefined-outer-name


@pytest.fixture()
def noonce():
    return "random_noonce"


@pytest.fixture()
def sso_key():
    return force_bytes(settings.DISCOURSE_SSO_KEY)


@pytest.fixture()
def sso_contents(noonce, sso_key):
    sso = base64.b64encode(urlencode({'nonce': noonce}).encode('ascii')) + b'\n'
    sig = force_bytes(hmac.new(sso_key, force_bytes(sso), digestmod=hashlib.sha256).hexdigest())
    return {
        "sig": sig,
        "sso": sso
    }


def test_view(admin_client: Client, sso_contents):
    response = admin_client.get(reverse('sso'), data=sso_contents)
    assert response.status_code == 302
    expected_response = (
        "http://localhost/test?sso=bm9uY2U9cmFuZG9tX25vb25jZ"
        "SZlbWFpbD1hZG1pbiU0MGV4YW1wbGUuY29tJnVzZXJuYW1lPWFk"
        "bWluJmV4dGVybmFsX2lkPTE%3D&sig=f79d43aba7fe196c1f3b"
        "533ca9f49cabdf09d49dccda7376524a759b364f56ee"
    )
    assert response.url == expected_response


def test_view_empty_get(admin_client: Client):
    response = admin_client.get(reverse('sso'), data={})
    assert response.status_code == 400


def test_invalid_data(admin_client: Client):
    response = admin_client.get(reverse('sso'), data={
        "sso": "bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGI=\n",
        "sig": "invalid_sig"
    })
    assert response.status_code == 400


def test_view_no_newline(admin_client: Client):
    response = admin_client.get(reverse('sso'), data={
        "sso": "bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGI=",
        "sig": "invalid_sig"
    })
    assert response.status_code == 400

