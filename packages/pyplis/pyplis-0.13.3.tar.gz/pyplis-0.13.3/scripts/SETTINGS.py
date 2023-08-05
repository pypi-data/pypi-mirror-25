# -*- coding: utf-8 -*-
"""
Global settings for example scripts
"""
from pyplis.inout import find_test_data
from pyplis import __version__, LineOnImage
from numpy import subtract
from os.path import join
from optparse import OptionParser
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'font.size': 13})

# the pyplis version for which these scripts
SCRIPTS_VERSION = "0.13"

SAVEFIGS = 1 # save plots from this script in SAVE_DIR
DPI = 150 #pixel resolution for saving
FORMAT = "png" #format for saving

SCREENPRINT = 0 #show images on screen when executing script

# Image directory
IMG_DIR = join(find_test_data(), "images")

# Directory where results are stored

SAVE_DIR = join(".", "scripts_out")
#SAVE_DIR = r'D:/Dropbox/TEMP/jgliss_publications/pyplis/graphics/out_code/'

# Emission rate retrieval lines

#ORANGE LINE IN YOUNG PLUME
PCS1 = LineOnImage(345, 350, 450, 195, pyrlevel_def=1, 
                          line_id="young_plume", color="#e67300",
                          normal_orientation="left")

#BLUE LINE IN AGED PLUME
PCS2 = LineOnImage(80, 10, 80, 270, pyrlevel_def=1, 
                          line_id="old_plume", color="#1a1aff",
                          normal_orientation="left")
    
LINES = [PCS1, PCS2]

OPTPARSE = OptionParser(usage='')
OPTPARSE.add_option('--show', dest="show", default=SCREENPRINT)

def check_version():
    v_code = [int(x) for x in __version__.split(".")[:2]]
    v_scripts = [int(x) for x in SCRIPTS_VERSION.split(".")[:2]]
    if any(subtract(v_scripts, v_code)) != 0:
        raise Exception("Version conflict between pyplis installation (v%s) "
            "and version of example scripts used (v%s). Please "
            "update your pyplis installation or use the set of example "
            "scripts corresponding to your installation. "
            %(__version__, SCRIPTS_VERSION))    
    