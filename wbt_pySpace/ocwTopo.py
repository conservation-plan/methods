# -----------------------------------------------------------------------------
# Name:         ocwTopo.py
# Purpose:      Reveal micro-topography of Otter Creek Wetlands
#
# Author:       Jeff Howarth
# Created:      10/05/2021
# License:      Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# -----------------------------------------------------------------------------

import tools from WBT module
from WBT.whitebox_tools import WhiteboxTools
wbt = WhiteboxTools()

# Define the Whitebox working directory
# You will need to change the path below to your local path name

wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/methods/wbt_pySpace/data"

# Declare a name for our test data path

dem = "../testDEM/_02_testLidar.tif"
