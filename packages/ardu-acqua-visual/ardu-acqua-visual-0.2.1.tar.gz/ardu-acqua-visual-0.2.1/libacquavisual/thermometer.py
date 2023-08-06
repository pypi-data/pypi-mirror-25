"""
MODULE:       thermometer
PURPOSE:      visualize a thermometer
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and the INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

from __future__ import division
from visual import cylinder, sphere, materials, label

class Thermometer(object):
    """
    Create a thermometer and let it show the temperature.
    """

    def __init__(self, pos=(-20,0,10), axis=(0,5,1), radius=.5, length=0):
        """
        Construct it with a preset or given geometry.
        """
        # calibration (see: calibrate(value))
        self.zero = None

        # a cylinders length MUST NEVER be '0' in pvisual ...
        if length == 0:
            length = 0.000001

        # color and material
        self.hot_color = (1,0,0)
        ### for now say: below zero this liquid is expanding...
        self.cold_color = (0.4,0.4,1)
        opacity = 1
        material = materials.rough

        # visualize the reservoir
        self.reservoir = sphere(pos=pos, radius=radius*4, color=self.hot_color,\
                            opacity=opacity, material=material)
        # visualize the expander
        self.expander = cylinder(pos=pos, axis=axis, radius=radius,\
                            length=length, color=self.hot_color,\
                            opacity=opacity, material=material)
        # add a label
        p = self.calc_label_pos(pos)
        self.label = label(pos=p, text=u'T: 0.0\xb0C')

    def calc_label_pos(self, pos):
        """
        Explicit calculation of the label position to the
        lower right, relative to the main object.
        """
        p = (pos[0]+8,pos[1]+5,pos[2]+2)
        return p

    def calibrate(self, value):
        """
        Calibrate the sensor to a certain initial value.
        """
        # We are getting absolute values already
        # TODO - but maybe we want to set 0 for the liquid column
        pass

    def display_value(self, value):
        """
        Set the display to visualize the sensor measurement
        """
        if value > 0:
            s = "+"
            color = self.hot_color
        elif value == 0:
            # a cylinders length MUST NEVER be '0' in pvisual ...
            value = 0.000001
        else:
            # out of lack of a better idea at the moment:
            s = "-"
            value = abs(value)
            color = self.cold_color

        self.reservoir.color = color
        self.expander.color = color
        self.expander.length = value / 2
        self.label.text = u'T: ' + s + str(value) + u'\xb0C'

    def clean_up(self):
        """
        Clean up the display
        """
        self.expander.visible = False
        self.reservoir.visible = False
        self.label.visible = False

