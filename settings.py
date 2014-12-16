# -*- coding: utf-8 -*-

# === Project Helper Commands ===

"""
The manage.py file relies on the click library for
some quick setup managment tasks via cli

Earthquakes.helpers

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: Simple helper functions to use in the management
commands

Check requirements for all needed cheeseshop installs

Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

import click

FEED_URL = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson'


def msg(msg=None, level='info'):

    """
    Prints a simple color coded message based on provided level

    This function acts a simple syntacal sugar helper for printing
    messages using the [click] library.

    Examples:
        Examples with and without level added

        msg('Your info message here')
        msg('Your error message here', 'error')
    """

    levels = dict(success='green', warning='yellow', error='red', info='cyan')
    return click.echo(click.style('{}'.format(msg), fg=levels[level]))

