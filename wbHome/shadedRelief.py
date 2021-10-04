# -----------------------------------------------------------------------------
# Name:         shadedRelief.py
# Purpose:      Shaded relief maps
#
# Author:       Jeff Howarth
# Created:      10/04/2021
# License:      Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# -----------------------------------------------------------------------------

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Define the Whitebox working directory
# You will need to change the path below to your local path name

wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/reland-tools/wbHome/data"

# Declare a name for our test data path

dem = "../testDEM/_02_testLidar.tif"


wbt.slope(dem,"_slope_degrees.tif",None,"degrees") # Slope in degrees
wbt.hillshade(dem, "_hillshade.tif",315.0,30.0,None) # Analytic hillshade
wbt.multidirectional_hillshade(dem, "_hillshadeMulti.tif", 45.0, None, False) # Multi-directional hillshade
