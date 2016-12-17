# Nexusadspy

A thin Python wrapper on top of the Appnexus API.

## Status

[![PyPI version](https://badge.fury.io/py/nexusadspy.svg)](https://badge.fury.io/py/nexusadspy)
[![Build Status](https://travis-ci.org/markovianhq/nexusadspy.svg)](https://travis-ci.org/markovianhq/nexusadspy)
[![codecov](https://codecov.io/gh/markovianhq/nexusadspy/branch/master/graph/badge.svg)]
(https://codecov.io/gh/markovianhq/nexusadspy)
[![Join the chat at https://gitter.im/markovianhq/Lobby](https://badges.gitter.im/markovianhq/Lobby.svg)]
(https://gitter.im/markovianhq/Lobby)
[![Documentation Status](https://readthedocs.org/projects/nexusadspy/badge/?version=latest)]
(https://nexusadspy.readthedocs.io/en/latest/?badge=latest)

## Installation

    $ pip install nexusadspy

## Usage Example

Set your developer username and password in the environment:

    $ export USERNAME_NEXUSADSPY='...'
    $ export PASSWORD_NEXUSADSPY='...'

To query the API for a list of all our advertisers:

    from nexusadspy import AppnexusClient
    client = AppnexusClient('.appnexus_auth.json')
    r = client.request('advertiser', 'GET')

To download data on just one of your advertisers, simply pass their ID
in the request:

    r = client.request('advertiser', 'GET', data={'id': 123456})

See [the documentation](https://nexusadspy.readthedocs.io) for more examples.
