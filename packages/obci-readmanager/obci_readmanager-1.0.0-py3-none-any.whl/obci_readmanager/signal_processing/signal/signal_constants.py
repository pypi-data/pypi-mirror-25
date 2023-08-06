"""
Module providing constants for data proxy.

Author:
     Mateusz Kruszyński <mateusz.kruszynski@gmail.com>
"""
import numpy

SAMPLE_SIZES = {'DOUBLE': 8, 'FLOAT': 4}
SAMPLE_STRUCT_TYPES = {'DOUBLE': 'd', 'FLOAT': 'f'}
SAMPLE_NUMPY_TYPES = {'DOUBLE': numpy.float64, 'FLOAT': numpy.float32}
