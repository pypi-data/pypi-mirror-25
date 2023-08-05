#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from astropy import time
from astropy.io import fits as pf
from astropy.table import Table
from .baseinstrument import Instrument
from ..utils.decorators import _autogen_docstring_inheritance
from ..utils.tools import kwargs_update

print "LRIS instrument not quite finished yet"

__all__ = ["lris"]

LRIS_INFO = {         
    }

# -------------------- #
# - Instrument Info  - #
# -------------------- #  
def lris(*args,**kwargs):
    return LRIS(*args,**kwargs)

def is_lris_file(filename):
    """This test if the given file is an LRIS one"""
    return pf.getheader(filename).get("INSTRUME") == "LRIS"

def which_band_is_file(filename):
    """
    """
    if not is_lris_file(filename):
        return None
    return pf.getheader(filename).get("FILTER")

########################################
#                                      #
# LRIS INSTRUMENT CLASS                 #
#                                      #
########################################    
class LRIS( Instrument ):
    """This is the umage object custom for LRIS data"""
    
    instrument_name = "LRIS"

    PROPERTIES         = ["LRIS"]
    SIDE_PROPERTIES    = []
    DERIVED_PROPERTIES = []
    
    def __build__(self,**kargs):
        """  """
        super(LRIS,self).__build__()
        # -- How to read the image
        self._build_properties = kwargs_update(self._build_properties,
                                               **dict(
                    header_exptime = "TOTALEXP"
                    ))

    # ------------------------ #
    # - Speciality           - #
    # ------------------------ #
   
    # =========================== #
    # = Properties and Settings = #
    # =========================== #    
    # --------------
    # - Image Data
    @property
    def exposuretime(self):
        if self._side_properties['exptime'] is None:
            # -- It has not be set manually, maybe check the header
            self._side_properties['exptime'] = \
              np.float(self.header[self._build_properties["header_exptime"]])
              
        # -- You have it ? This will stay None if not
        return self._side_properties['exptime']
    
    @property
    def bandname(self):
        if self.header is None:
            raise AttributeError("no header loaded ")
        print "WARNING SDSS-like filter used"
        return "sdss"+self.header["FILTER"]

    # --------------------
    # - Band Information
    @property
    def mjd(self):
        """This is the Modify Julien Date at the start of the Exposure"""
        return time.Time(self.header["JDSTART"], format="jd").mjd

    @property
    def mab0(self):
        """zeropoint in ABmag
        http://www.stsci.edu/hst/wfc3/phot_zp_lbn
        ABMAG_ZEROPOINT = -2.5 Log (PHOTFLAM) - 21.10 - 5 Log (PHOTPLAM) + 18.6921 
        """
        return self.header["ZEROPT0"]
          
    # -------------------
    # - Instrument Info

    # ------------------------
    # - Image Data Reduction
    @property
    def _gain(self):
        """This is the calibrated gain"""
        return self.header["GAIN"]
    
    @property
    def _readnoise(self):
        """This is the calibrated read noise"""
        return None
    
    @property
    def _biaslevel(self):
        return None

