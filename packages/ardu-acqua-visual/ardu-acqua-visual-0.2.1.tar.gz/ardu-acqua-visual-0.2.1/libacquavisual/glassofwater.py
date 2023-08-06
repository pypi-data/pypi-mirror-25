"""
MODULE:       glassofwater
PURPOSE:      visualize a glass of water
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and the INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

from __future__ import division
from visual import cylinder, materials, label

class GlassOfWater(object):
    """
    Create a transparent glass and let it be filled with
    water.
    """

    def __init__(self, pos=(12,-16,8), axis=(0,5,1), radius=6, length=20):
        """
        Construct it with a preset or given geometry.
        """
        # calibration (see: calibrate(value))
        self.zero = 0
        self.correction = 0

        # a cylinders length MUST NEVER be '0' in pvisual ...
        # and in our case not below the zero point: empty is empty..
        if length <= 0:
            length = 0.001

        # color and material
        glass_color = (0,1,1)
        liquid_color = (0,0.8,1)
        glass_opacity = 0.5
        liquid_opacity = 0.5
        glass_material = materials.rough
        liquid_material = materials.rough

        # visualize the empty container
        self.glass = cylinder(pos=pos, axis=axis, radius=radius, length=length,\
                            color=glass_color, opacity=glass_opacity,\
                            material=glass_material)
        # visualize the liquid (just a little to start with)
        self.liquid = cylinder(pos=pos, axis=axis, radius=radius, length=.1,\
                            color=liquid_color, opacity=liquid_opacity,\
                            material=liquid_material)
        # add a label
        p = self.calc_label_pos(pos)
        self.label = label(pos=p, text='W: 0.0cm')

    def calc_label_pos(self, pos):
        """
        Explicit calculation of the label position to the
        lower right, relative to the main object.
        """
        p = (pos[0]+8,pos[1]+5,pos[2]+2)
        return p

    def calibrate(self, value, zero=None):
        """
        Calibrate the sensor to a certain initial value.
        Assumption: The sensor is delivering an approximation already and
            we have to calculate only the difference.
        TODO later we might want to have more than one calibration methods..
        """
        # set it or leave it
        if zero is not None:
            self.zero = zero
        # the expected zero value to compare to zero at the time of measuremnt
        self.correction = self.zero - value

    def display_value(self, value):
        """
        Set the display to visualize the sensor measurement
        """
        v = (self.zero - self.correction - value) * 100
        if v <= 0:
            # a cylinders length MUST NEVER be '0' in pvisual ...
            # and in our case not below the zero point: empty is empty..
            v = 0.001
            self.label.text='W: 0.0cm'
        else:
            self.label.text='W: ' + str(v) + 'cm'
        self.liquid.length = v

    def clean_up(self):
        """
        Clean up the display
        """
        self.glass.visible = False
        self.liquid.visible = False
        self.label.visible = False

