# Nexusadspy

A thin Python wrapper on top of the Appnexus API.

See usage examples below!

## Status

[![PyPI version](https://badge.fury.io/py/nexusadspy.svg)](https://badge.fury.io/py/nexusadspy)
[![Build Status](https://travis-ci.org/markovianhq/nexusadspy.svg)](https://travis-ci.org/markovianhq/nexusadspy)

## Installation

### Installation as regular library

Install the latest release from PyPI:

    $ pip install nexusadspy

To install the latest `master` branch commit of nexusadspy:

    $ pip install -e git+git@github.com:markovianhq/nexusadspy.git@master#egg=nexusadspy

To install a specific commit, e.g. `97c41e9`:

    $ pip install -e git+git@github.com:markovianhq/nexusadspy.git@97c41e9#egg=nexusadspy

### Installation for development

To install nexusadspy for local development you may want to create a virtual environment.
Assuming you use [Continuum Anaconda](https://www.continuum.io/downloads), create
a new virtual environment as follows:

    $ conda create --name nexusadspy python=3 -y

Activate the environment:

    $ source activate nexusadspy

Install the requirements:

    $ pip install -y -r requirements.txt

Now install nexusadspy in development mode:

    $ python setup.py develop

To run the tests, install these additional packages:

    $ pip install -r requirements_test.txt

Now run the tests:

    $ py.test nexusadspy --flake8

## Examples

Set your developer username and password in the environment:

    $ export USERNAME_NEXUSADSPY='...'
    $ export PASSWORD_NEXUSADSPY='...'

For convenience, place the above two lines in an environment file,
e.g. `nexusadspy.env`:

    # nexusadspy.env
    export USERNAME_NEXUSADSPY='...'
    export PASSWORD_NEXUSADSPY='...'

And source this file as follows:

    $ source nexusadspy.env

### Sample API service query

Pick one of the Appnexus services to interact with off
[this list](https://wiki.appnexus.com/display/api/API+Services).

Here we will query the API for a list of all our advertisers and we
will store temporarily our authentication token in a hidden file
`.appnexus_auth.json`:

    from nexusadspy import AppnexusClient
    client = AppnexusClient('.appnexus_auth.json')
    r = client.request('advertiser', 'GET')

To download data on just one of your advertisers, simply pass their ID
in the request:

    r = client.request('advertiser', 'GET', data={'id': 123456})

### Sample reporting query

In the following example we set up an `attributed_conversions` report
for the period starting on Oct 1, 2015 and ending on Nov 1, 2015 
for the advertiser with ID `123456`.

    from nexusadspy import AppnexusReport

    columns = ["datetime",
               "pixel_name",
               "pixel_id",
               "post_click_or_post_view_conv",
               "line_item_name",
               "line_item_id",
               "campaign_id",
               "imp_time",
               "advertiser_id"]

    report_type = "attributed_conversions"

    filters = [{"imp_type_id":{"operator":"!=","value": 6}}]

    report = AppnexusReport(advertiser_ids=123456,
                            start_date='2015-10-01',
                            end_date='2015-11-01',
                            filters=filters,
                            report_type=report_type,
                            columns=columns)

To trigger and download the report just run the `get` method on your `report`:

    output_json = report.get()

In case you have `pandas` installed you can also request the report as a
dataframe as follows:

    output_df = report.get(format_='pandas')

### Sample segments upload

In the following example, we upload a list of users to user segment `my_segment_code`
using the [batch segment upload service](https://wiki.appnexus.com/display/api/Batch+Segment+Service).
We assume that the segment `my_segment_code` has already been created in the corresponding account.
The respective users also need to be pixelled on AppNexus from your website before they can be added to segments.

    from nexusadspy.segment import AppnexusSegmentsUploader

    # List of five separators obtained from Appnexus support
    my_separators_list = [':',';','^','~',',']

    seg_code = "my_segment_code"
    my_member_id = "1234"

    members = [
        {"uid": "0123456789012345678", "timestamp": "1447952642"},
        {"uid": "9876543210987654321", "timestamp": "1447921128"},
        {"uid": "1122334455667788990", "timestamp": "1447914439"}
    ]

    uploader = AppnexusSegmentsUploader(members, seg_code, my_spearators_list, my_member_id)

To trigger the upload, run `upload()` method on `uploader`:

    upload_status = uploader.upload()
