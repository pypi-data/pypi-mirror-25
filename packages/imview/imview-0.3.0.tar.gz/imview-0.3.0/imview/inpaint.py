#! /usr/bin/env python

import sys
import os

import numpy as np
from skimage.restoration import inpaint_biharmonic

from pygeotools.lib import iolib

def normalize(dem):
    return dem2

dem_fn = sys.argv[1]
dem = iolib.fn_getma(dem_fn)
mask = np.ma.getmaskarray(dem)

min=dem.min()
max=dem.max()
ptp=max - min
new_ndv = dem.min() - ptp/32768.
dem2 = dem.filled(new_ndv)
dem2 = dem2/max 

dem_filled = inpaint_biharmonic(dem2, mask)
#dem_filled_fn = os.path.splitext(dem_fn)[0]+'_inpaint.tif'
#iolib.writeGTiff(dem, dem_filled_fn, dem_fn)
