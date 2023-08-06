# -*- coding: utf-8 -*-
"""Wii utils."""


def get_x_y(tl, tr, br, bl):
    """For given wii sensor values:.

    - tl - top left
    - tr - top right
    - br - bottom right
    - bl - bottom left
    in int or float format, return x, y in floats.
    """
    sum_mass = tl + tr + br + bl
    x = (((tr + br) - (tl + bl)) / sum_mass)
    y = (((tr + tl) - (br + bl)) / sum_mass)
    return x, y
