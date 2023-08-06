Conference Scehduler Command Line Interface
===========================================
A command line tool to manage the schedule for a conference.

Installation
============

The library requires Python 3.6 or later. The simplest way to install is::

    pip install conference-scheduler-cli

To install from source code::

    git clone https://github.com/PyConUK/ConferenceScheduler-cli
    cd ConferenceScheduler-cli
    python setup.py install

Quick Start
===========

The tool expects to find a directory with the necessary data files to define
the conference. By default it will look for a directory named `input` under
the current working directory.

It will generate YAML files in the format required by the conference
website. By default, these will be placed a in a `build` directory under the
current working directory.

It will also generate `.csv` and `.pickle` files to store the calculated
schedule and its associated definition and a log file with the full details of
the most recent calculation. By default, these will be placed in a
`solution` directory under the current working directory.

The `input`, `solution` and `build` directories can be passed to the tool as
command line options in place of the default locations.

To build the schedule with the default options::

    scheduler build

There are also further options, e.g. to set the logging verbosity or the
solver algorithm to use. To view those options::

    scheduler --help

or, for the options for a specifc command::

    scheduler build --help
