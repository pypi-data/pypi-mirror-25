"""
MODULE:       hygrometer
PURPOSE:      visualize a hygrometer
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and the INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

from __future__ import division
from visual import box, materials, label

class Hygrometer(object):
    """
    Create a box visualizing the relative humidity.
    """

    def __init__(self, pos=(-20,-10,10), axis=(0,5,1), length=8, height=8,\
                                                                    width=8):
        """
        Construct it with a preset or given geometry.
        """
        # calibration (see: calibrate(value))
        self.zero = None

        # color and material
        room_color = (1,1,1)
        wet_color = (0,0,1)
        room_opacity = 0.5
        wet_opacity = 0.5
        room_material = materials.diffuse
        wet_material = materials.diffuse

        ## NOTE: do not change the order here, or self.wet will never be
        #        seen again.. (even with opaque, vpython hides the second cube)
        # visualize the humidity
        self.wet = box(pos=pos, axis=axis, length=length, height=height,\
                        width=width, opacity=wet_opacity, color=wet_color,\
                        material=wet_material)
        # visualize the empty space
        self.room = box(pos=pos, axis=axis, length=length, height=height,\
                        width=width, opacity=room_opacity, color=room_color,\
                        material=room_material)
        # add a label
        p = self.calc_label_pos(pos)
        self.label = label(pos=p, text='H: 100%')

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
        pass

    def display_value(self, value):
        """
        Set the display to visualize the sensor measurement
        """
        v = value / 10
        self.wet.length = v
        self.wet.height = v
        self.wet.width = v
        self.label.text = 'H: ' + str(value) + '%'

    def clean_up(self):
        """
        Clean up the display
        """
        self.room.visible = False
        self.wet.visible = False
        self.label.visible = False

