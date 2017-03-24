# -*- coding: utf-8 -*-

from __future__ import (
    print_function, division, generators,
    absolute_import, unicode_literals
)

import os

import pytest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from nexusadspy import AppnexusClient
from nexusadspy.exceptions import NexusadspyConfigurationError


def test_failure_no_credentials():
    try:
        os.environ['USERNAME_NEXUSADSPY']
        os.environ['PASSWORD_NEXUSADSPY']
    except KeyError:
        with pytest.raises(NexusadspyConfigurationError) as excinfo:
            client = AppnexusClient('.appnexus_auth.json')
            client._get_new_auth_token()

            assert 'set environment variables' in str(excinfo.value.lower())


def test_http_methods():
    with patch.object(AppnexusClient, "_do_paged_get", autospec=True) as mock_paged:
        with patch.object(AppnexusClient, "_do_authenticated_request", autospec=True) as mock_auth:
            mock_auth.return_value = (200, {})
            mock_paged.return_value = (200, {})
            client = AppnexusClient("foo")
            client.request("bar", "get")
            assert mock_auth.call_count == 0
            mock_paged.assert_called_once_with(client, client.endpoint + "/bar", "get",
                                               data={}, get_field=None, headers=None, params={})

    with patch.object(AppnexusClient, "_do_paged_get", autospec=True) as mock_paged:
        with patch.object(AppnexusClient, "_do_authenticated_request", autospec=True) as mock_auth:
            mock_auth.return_value = (200, {})
            mock_paged.return_value = (200, {})
            client = AppnexusClient("bar")
            client.request("foo", "post")
            mock_auth.assert_called_once_with(client, client.endpoint + "/foo", "post",
                                              data={}, headers=None, params={})
            assert mock_paged.call_count == 0

    with patch.object(AppnexusClient, "_do_paged_get", autospec=True) as mock_paged:
        with patch.object(AppnexusClient, "_do_authenticated_request", autospec=True) as mock_auth:
            mock_auth.return_value = (200, {})
            mock_paged.return_value = (200, {})
            client = AppnexusClient("pfoo")
            client.request("pbar", "put")
            mock_auth.assert_called_once_with(client, client.endpoint + "/pbar", "put",
                                              data={}, headers=None, params={})
            assert mock_paged.call_count == 0

    with patch.object(AppnexusClient, "_do_paged_get", autospec=True) as mock_paged:
        with patch.object(AppnexusClient, "_do_authenticated_request", autospec=True) as mock_auth:
            mock_auth.return_value = (200, {})
            mock_paged.return_value = (200, {})
            client = AppnexusClient("dfoo")
            client.request("dbar", "delete")
            mock_auth.assert_called_once_with(client, client.endpoint + "/dbar", "delete",
                                              data={}, headers=None, params={})
            assert mock_paged.call_count == 0


def test_wrong_http_methods():
    client = AppnexusClient("foo")
    with pytest.raises(ValueError) as excinfo:
        client.request("bar", "wget")
        assert excinfo.value.lower() == 'Argument "method" must be one of ' \
            '["get", "post", "put", "delete"]. You supplied: "wget".'


def test_development_mode_get():
    client = AppnexusClient("foo", mode='development')

    with patch.object(AppnexusClient, '_do_paged_get') as method:
        method.return_value = (200, {})
        client.request('some_service', 'get')

        method.assert_called_once()


def test_development_mode_non_get():
    client = AppnexusClient("foo", mode='development')
    methods = ['post', 'put', 'delete']

    for method in methods:
        res = client.request('some_service', method)

        assert res[0]['response']['status'] == 'ok'
        assert 'development' in res[0]['response']['message']
