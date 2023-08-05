# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 10:52:27 2017

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""


###########################################################################
#::: import standard/community packages
########################################################################### 
import os
import numpy as np
import matplotlib.pyplot as plt


###########################################################################
#::: import my custom packages
########################################################################### 
from mytools import lightcurve_tools


###########################################################################
#::: import sub-packages
########################################################################### 
#import stacked_images
#from astropy.stats import LombScargle
#from scipy.signal import lombscargle
#import lightcurve_tools, get_scatter_color



#def load_stacked_image(C):
#    '''
#    C              centroid class, passed over as 'self' from centroiding.py
#    '''
#    
#    refcatdir = 'RefCatPipe*' + C.fieldname + 
#    filename = glob.glob( os.path.join( C.root, 'DITHERED_STACK_'+fieldname+'*.fits' ) )[-1]
#    RefCatPipe_P.5046627_F.NG1318-4500_C.811_A.118433_T.REFCAT1706A
#    data = fitsio.read( C.stacked_image_filename )
    
    

###########################################################################
#::: plot
########################################################################### 
def plot(C, blend_radius=6):
    '''
    C              centroid class, passed over as 'self' from centroiding.py
    blend_radius   for an aperture of 3 pixels and PSF of ~1 pixel, we assume
                   only objects <=6 pixels away will blend into the photometric aperture of the target
    '''
    ind_blends = np.where( (np.abs(C.dic_nb['CCDX_0'] - C.dic['CCDX_0']) < blend_radius) & \
                          (np.abs(C.dic_nb['CCDY_0'] - C.dic['CCDY_0']) < blend_radius) )[0]
    N_blends = len(ind_blends)
    
    fig, axes = plt.subplots( np.max((N_blends,1)), 3, figsize=(15,np.max((N_blends,1))*4) )
    
    for i in ind_blends:
        #::: plot CCD locations of target and all neighbours
        axes[i,0].plot( C.dic['CCDX_0'], C.dic['CCDY_0'], 'bo', ms=12 )
        axes[i,0].plot( C.dic_nb['CCDX_0'], C.dic_nb['CCDY_0'], 'k.' )
        axes[i,0].plot( C.dic_nb['CCDX_0'][i], C.dic_nb['CCDY_0'][i], 'ro', ms=12 )
        axes[i,0].set( xlim=[ C.dic['CCDX'][0]-10, C.dic['CCDX'][0]+10 ], ylim=[ C.dic['CCDY'][0]-10, C.dic['CCDY'][0]+10 ] )        
        circle1 = plt.Circle((C.dic['CCDX_0'], C.dic['CCDY_0'],), 3, color='r', fill=False, linewidth=3)
        axes[i,0].add_artist(circle1)
        
        #::: plot phase folded lightcurve of selected neighbour
        hjd_phase, flux_phase, _, _, _ = lightcurve_tools.phase_fold(C.dic_nb['HJD'][i], C.dic_nb['SYSREM_FLUX3'][i], C.dic['PERIOD'], C.dic['EPOCH'], dt = C.dt, ferr_type='meansig', ferr_style='sem', sigmaclip=True)
        axes[i,1].plot( hjd_phase, flux_phase, 'bo', rasterized=True )
 
    outfilename = os.path.join( C.outdir, C.fieldname + '_' + C.obj_id + '_' + C.ngts_version + '_blends.pdf' )   
    plt.savefig( outfilename )