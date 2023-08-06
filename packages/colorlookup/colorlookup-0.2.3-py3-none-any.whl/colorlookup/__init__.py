# -*- coding: utf-8 -*-
"""W3C standard color lookup tool.

This package provides an API for looking up hex, rgb, hsv, or hsl values of
W3C-recognized colors. The Color class, when initialized with a valid
identifier, will have as its attributes components of the various color model
representations.

Example:
    To retrieve the numeric representations of the color brown as defined by
    the W3C::
        ```python3
        >>> from colorlookup import Color
        >>>
        >>> brown = Color('brown')
        >>>
        >>> print(brown)
        Color: Brown
          hex: #a52a2a
          rgb: (165, 42, 42)
        >>>
        >>> brown.hex
        '#a52a2a'
        >>> brown.rgb
        (165, 42, 42)
        >>> brown.r
        165
        >>> brown.g
        42
        >>> brown.b
        42
        >>> brown.rgb_f
        (0.65, 0.16, 0.16)
        >>> brown.r_f
        0.65
        >>> brown.g_f
        0.16
        >>> brown.b_f
        0.6
        >>> brown.hsl_sat
        0.59
        >>> brown.hsl_light
        0.41
        >>> brown.hsv_sat
        0.75
        >>> brown.hsv_val
        0.65

        ```
"""

import os.path
import sqlite3

DB_FILE = os.path.join(os.path.dirname(__file__), 'colors.db')

def hex_to_rgb(val):
    """Convert hex value to RGB triplet.

    Helper function that converts a hex *string*, with or without identifying
    prefix, to a 3-tuple of single-byte unsigned integers (0-255).

    Args:
        val (str): A 24 bit color hex string in the form RRGGBB. It may include a
            prefix (#, 0x), but does not need to.

    Returns:
        tuple: A 3-tuple of single byte, unsigned integers (0-255) representing
            the red, green, and blue values of the color respectively.
    """
    if val.startswith('#'):
        val = val[1:]
    # r = round(int(val[:2], 16) * 100 / 255.0, 0) / 100.0
    # g = round(int(val[2:4], 16) * 100 / 255.0, 0) / 100.0
    # b = round(int(val[4:6], 16) * 100 / 255.0, 0) / 100.0
    r = int(val[:2], 16)
    g = int(val[2:4], 16)
    b = int(val[4:6], 16)
    return(r, g, b)

class Color:
    """Class representing a single W3C-recognized color.

    A Color object has as its attributes a component of, or the entire
    representation of a color model representing its color.

    Attributes:
        key (str): The W3C name for the given color. W3C names are all lower
            case and don't contain any spaces.
        name (str): A more readable name for the color. This is usually just
            the key with title capitalizatioin and spaces inserted.
        hex (str): A string representation of the 3 byte RGB color model value.
            The hex string is prefixed by '#' and in the form RRGGBB.
        hue (int): Angle in degrees of the hue in both the HSL and HSV color
            models.
        hsl_sat (float): The saturation of the color in the HSL color model.
            (0-1)
        hsl_light (float): The lightness of the color in the HSL color model.
            (0-1)
        hsv_sat (float): The saturation of the color in the HSV color model.
            (0-1)
        hsv_val (float): The value of the color in the HSV color model. (0-1)
    """
    _con = sqlite3.connect(DB_FILE)

    def __init__(self, key):
        """Initialize a Color object representing a W3C color.

        Args:
            key (str): Key/name of the color. This argument is case insensitive
            and can be either the W3C format (no spaces) or readable format
            (with spaces).

        Raises:
            KeyError: Raised if no matching color is found.
        """
        cur = Color._con.cursor()
        cur.execute('SELECT * FROM w3c_colors WHERE key=?',
                    (key.replace(' ', '').lower(),))
        rec = cur.fetchone()

        if not rec:
            raise KeyError(key)

        self.key = rec[0]
        self.hex = '#' + str(hex(rec[1])[2:]).zfill(6)
        self.name = rec[2]
        self.hue = int(rec[3])
        self.hsl_sat = float(rec[4]) / 100
        self.hsl_light = float(rec[5]) / 100
        self.hsv_sat = float(rec[6]) / 100
        self.hsv_val = float(rec[7]) / 100

    @property
    def r(self):
        """int: A single-byte unsigned integer (0-255) representing the red
            value in the RGB color model.
        """
        return int(self.hex[1:3], 16)

    @property
    def r_f(self):
        """int: A float (0-1) representing the red value in the RGB color
            model.
        """
        return round(self.r / 255.0, 2)

    @property
    def g(self):
        """int: A single-byte unsigned integer (0-255) representing the green
            value in the RGB color model.
        """
        return int(self.hex[3:5], 16)

    @property
    def g_f(self):
        """int: A float (0-1) representing the green value in the RGB color
            model.
        """
        return round(self.g / 255.0, 2)

    @property
    def b(self):
        """int: A single-byte unsigned integer (0-255) representing the blue
            value in the RGB color model.
        """
        return int(self.hex[5:7], 16)

    @property
    def b_f(self):
        """int: A float (0-1) representing the blue value in the RGB color
            model.
        """
        return round(self.b / 255.0, 2)

    @property
    def rgb(self):
        """tuple of int: A 3 tuple containing the color's r, g, and b
            attributes.
        """
        return (self.r, self.g, self.b)

    @property
    def rgb_f(self):
        """tuple of float: A 3 tuple containing the color's r_f, g_f, and b_f
            attributes.
        """
        return (self.r_f, self.g_f, self.b_f)

    def __repr__(self):
        return 'Color: ' + self.name + '\n' + \
               '  hex: ' + self.hex + '\n' + \
               '  rgb: ' + str(self.rgb)
