#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class IntegratedHingeBox(Boxes):
    """Box with lid and integraded hinge"""

    ui_group = "Box"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(edges.ChestHingeSettings)
        self.buildArgParser("x", "y", "h", "outside")
        self.argparser.add_argument(
            "--lidheight",  action="store", type=float, default=20.0,
            help="height of lid in mm")
        

    def render(self):

        x, y, h, hl = self.x, self.y, self.h, self.lidheight
        if hl < 30:
            raise ValueError("unable to draw limiters with lidheight < 30")

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        t = self.thickness

        hy = self.edges["O"].startwidth()
        hy2 = self.edges["P"].startwidth()

        e1 = edges.CompoundEdge(self, "Fe", (h-hy, hy))
        e2 = edges.CompoundEdge(self, "eF", (hy, h-hy))
        e_back = ("F", e1, "e", e2)

        self.rectangularWall(y, h-hy, "FfOf", ignore_widths=[2], move="up")
        self.rectangularWall(y, hl-hy2, "pfFf", ignore_widths=[1], move="up",
                callback=[lambda: self.fingerHolesAt(hy, 1.5*t-hy2, y-hy2, 0)])
        self.rectangularWall(y, h-hy, "Ffof", ignore_widths=[5], move="up")
        self.rectangularWall(y, hl-hy2, "PfFf", ignore_widths=[6], move="up",
                callback=[lambda: self.fingerHolesAt(0, 1.5*t-hy2, y-hy2, 0)])

        # screen door
        d1 = edges.CompoundEdge(self, "fe", (y-hy, hy))
        d2 = edges.CompoundEdge(self, "ef", (hy, y-hy))
        e_door = (d1, "f", d2, "f")
        self.rectangularWall(y, x, e_door, move="up")

        self.rectangularWall(x, h, "FFeF", move="up")

        # bottom back
        def back_support():
            self.fingerHolesAt(5, 0, hl, 90)
            self.fingerHolesAt(x-5, 0, hl, 90)
        self.rectangularWall(x, h, e_back, move="up",
                callback=[None, None, back_support])

        # screen frontside
        self.rectangularWall(x, hl, "FFeF", move="up",
                callback=[None, None, lambda: self.fingerHolesAt(0, 1.5*t, x, 0)])

        # screen back
        self.rectangularWall(x, hl-hy2, "FFqF", move="up",
                callback=[None, None, lambda: self.fingerHolesAt(0, 1.5*t-hy2, x, 0)])

        self.rectangularWall(y, x, "ffff", move="up")
        self.rectangularWall(y, x, "ffff", move="up")

        # screen holders
        for i in range(0, 2):
            self.moveTo(0, hl, 270)
            self.polyline(hl, 100)
            self.edges["f"](hl)
            self.polyline(0, 90, 0, (80, hl), 0, 90)
            self.moveTo(0, hl)

