This package provides an API for looking up hex, rgb, hsv, or hsl values of
W3C-recognized colors. The Color class, when initialized with a valid
identifier, will have as its attributes components of the various color model
representations.

Example:
    To retrieve the numeric representations of the color brown as defined by
    the W3C::
    .. code:: python3
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


