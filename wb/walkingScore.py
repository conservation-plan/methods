# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:    walkingScore.py
#  purpose: Compute total amount of time to walk to nearest trailhead
#
#  author:   Brooke Laird & Jeff Howarth
#  update:   12/12/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = "/Volumes/LaCie/GEOG0310/wbt_pySpace/lPublicAccess/data"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Test datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rds = "iRdsAccess.tif"
origin_pt = "iTrailHeads.tif"


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Buffer roads and classify friction values
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wbt.buffer_raster(
    i = rds,
    output = "01_rds_buffer.tif",
    size = 2,
    gridcells=True
)

#reclass road into friction values

wbt.reclass(
    i = "01_rds_buffer.tif",
    output = "03_rds_float_reclass.tif",
    reclass_vals = "3.36;0.0;1.68;1.0",
    assign_mode=True
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Cost Distance Analysis
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wbt.cost_distance(
    source = origin_pt, #what is your origin point raster?
    cost = "03_rds_float_reclass.tif",
    out_accum = "_costAccumulation.tif", #total cost of moving from origin to anywhere else
    out_backlink = "_backlink.tif" #how did you move
    #callback=default_callback
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Reclassify isopleths
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#For analysis of the output raster, visit the markdown documentation file
