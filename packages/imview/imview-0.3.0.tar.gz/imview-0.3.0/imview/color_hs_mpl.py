#! /usr/bin/env python

import sys
import os

import matplotlib.pyplot as plt

from pygeotools.lib import warplib, geolib, iolib, malib
from imview.lib import gmtColormap, pltlib
cpt_rainbow = gmtColormap.get_rainbow()
plt.register_cmap(cmap=cpt_rainbow)

"""
Create a color shaded relief map for an input DEM
"""

#Better to use warplib to make sure same extent?
dem_fn = sys.argv[1]
hs_fn = os.path.splitext(dem_fn)[0]+'_hs_az315.tif'

if not os.path.exists(hs_fn):
    #GDAL2.1 gdaldem utility as library
    #ds = gdal.DEMProcessing('', src_ds, 'hillshade', format='MEM', computeEdges=True)
    hs_fn = geolib.gdaldem_wrapper(dem_fn, 'hillshade', returnma=False)

dem_ds, hs_ds = warplib.memwarp_multi_fn([dem_fn, hs_fn], res='first', extent='first', t_srs='first')

print("Loading input DEM array")
dem = iolib.ds_getma(dem_ds)
print("Loading input hs array")
hs = iolib.ds_getma(hs_ds)

hs_cmap_name = 'gray'
dem_cmap_name = 'cpt_rainbow'
dem_clim_perc = (2, 98)
hs_clim_perc = (0.05, 99.95)
dem_alpha = 0.5
#imshow_kwargs={'interpolation':'bicubic'}
imshow_kwargs={'interpolation':'none', 'aspect':'equal'}
out_dpi = 300.0
out_figsize = (dem.shape[1]/out_dpi, dem.shape[0]/out_dpi)
dem_clim = None

if dem_clim is None:
    dem_clim = malib.calcperc(dem, dem_clim_perc)
hs_clim = malib.calcperc(hs, hs_clim_perc)

dem_cmap = plt.get_cmap(dem_cmap_name)
dem_cmap.set_bad(alpha=0)
hs_cmap = plt.get_cmap(hs_cmap_name)
hs_cmap.set_bad(alpha=0)

fig = plt.figure(figsize=out_figsize, dpi=out_dpi, frameon=False)
#This is necessary to take up the full figure size
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
hs_im = ax.imshow(hs, cmap=hs_cmap, clim=hs_clim, alpha=1.0, **imshow_kwargs)
dem_im = ax.imshow(dem, cmap=dem_cmap, clim=dem_clim, alpha=0.5, **imshow_kwargs)
#pltlib.hide_ticks(ax)
ax.set_adjustable('box-forced')
ax.set_axis_bgcolor('k')
fig.set_facecolor('k')

of = 'tif'
out_fn = os.path.splitext(dem_fn)[0]+'_fig.'+of
out_kwargs = {'dpi':out_dpi, 'bbox_inches':'tight', 'pad_inches':0, 'facecolor':fig.get_facecolor(), 'edgecolor':'none'}

#Save transparent figure
if of == 'png':
    out_kwargs['transparent'] = True

print("Saving output figure")
print('%0.1f x %0.1f @ %0.1f dpi\n' % (out_figsize[0], out_figsize[1], out_dpi))
fig.savefig(out_fn, **out_kwargs)

import gdal
out_ndv = 0

#out_ds = gdal.Open(out_fn, gdal.GA_Update)

"""
in_ds = gdal.Open(out_fn, gdal.GA_ReadOnly)
print("Creating copy")
out_ds = iolib.gtif_drv.CreateCopy(out_fn, in_ds, 0, options=iolib.gdal_opt) 
in_ds = None
out_ndv = 0
out_ds.SetGeoTransform(dem_ds.GetGeoTransform())
out_ds.SetProjection(dem_ds.GetProjection())
for n in range(out_ds.RasterCount):
    b = out_ds.GetRasterBand(n+1)
    b.SetNoDataValue(out_ndv)
print("Writing out")
"""

in_ds = gdal.Open(out_fn, gdal.GA_ReadOnly)
ns = in_ds.RasterXSize
nl = in_ds.RasterYSize
print("Create new")
out_fn2 = os.path.splitext(out_fn)[0]+'_new.tif'
out_ds = iolib.gtif_drv.Create(out_fn, ns, nl, bands=3, eType=gdal.GDT_Byte, options=iolib.gdal_opt) 
out_ds.SetGeoTransform(dem_ds.GetGeoTransform())
out_ds.SetProjection(dem_ds.GetProjection())
for n in range(out_ds.RasterCount):
    b = out_ds.GetRasterBand(n+1)
    b.WriteArray(in_ds.GetRasterBand(n+1).ReadAsArray())
    b.SetNoDataValue(out_ndv)
print("Writing out")
in_ds = None
out_ds = None
