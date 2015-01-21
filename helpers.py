# -*- coding: utf-8 -*-

"""
The manage.py file relies on the click library for some quick
setup managment tasks via cli

Earthquakes.helpers

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: helpers ...


Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

import click

# === Helper Methods ===

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
