# !/usr/bin/env python
# -*- coding: utf-8 -*-

# === Application : Earthquakes ===

"""
Application login file for for the Earthquakes
project

Earthquakes.uimodules

:author: Regi E. <regi@persona.io>
:created: 20141123
:desc: Handles all uimodules logic

Write your code as if the person maintaining it is a
Homicidal Maniac who knows where you live...

"""

from tornado.web import UIModule


class Quake(UIModule):

    def render(self, quake):
        return self.render_string("module_quake.html", quake=quake)
