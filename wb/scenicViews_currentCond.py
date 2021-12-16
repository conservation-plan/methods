# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   name:     scenicViews_currentCond.py
#  purpose:  Perform a viewshed analysis for the Town of Middebury.
#  author:  Alana Kornaker, co author Jeff Howarth
#  update:   12/06/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# Declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = "/Volumes/LaCie/GEOG0310/wbt_pySpace/lScenicViews/data"

# DATASETS

dem = "vizDEM2.tif"
pts = "scenicPoints.shp"
ptCount = 620.0
view = 'scenicVis2.tif'
viewP = 'scenicVisPercent2.tif'

# Step 4: VIEWSHED ANALYSIS

wbt.viewshed(
    dem = dem,
    stations = pts,
    output = view,
    height=1.8
)

wbt.divide(
    input1 = view,
    input2 = ptCount,
    output = viewP
)
