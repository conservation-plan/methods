# -----------------------------------------------------------------------------
# Name:         slopeClass.py
# Purpose:      Slope classification
#
# Author:       Jeff Howarth
# Created:      10/03/2021
# License:      Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# -----------------------------------------------------------------------------
# References:
#
# Schoeneberger et al, Landscapes, Geomorphology, and Site Description.
#   https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054252
#   Accessed 10/03/2021
#
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

# Slope in percent

wbt.slope(dem,"slope_percent.tif",None,"percent")

# Reclass slope with a table

wbt.reclass_from_file("slope_percent.tif","../slopeClass.txt",'_slopeClass.tif')
