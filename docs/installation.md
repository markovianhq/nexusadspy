# Installation

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

    $ pip install -r requirements.txt

Now install nexusadspy in development mode:

    $ python setup.py develop

To run the tests, install these additional packages:

    $ pip install -r requirements_test.txt

In case you are on Python 2.7, install the `mock` package:

    $ pip install mock

Now run the tests:

    $ py.test nexusadspy --flake8
