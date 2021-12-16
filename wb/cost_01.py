#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:     costDistance.py
#  purpose:  to compute cost distance in seconds
#
#  author:   Jeff Howarth
#  update:   11/16/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

# Full data
wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/cost"

# Test data
# wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/hb_test"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test datasets

rds = "rds_fragmenting.tif"       # Highways and Class 3 roads
lc = "lc_5m.tif"                  # 2016 Vermont base land cover

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# create blank raster as float (to force rasters to store decimal values)

wbt.new_raster_from_base(
    base = lc,
    output = "00_base.tif",
    value = "1",
    data_type = "float"
)

# convert lc to float

wbt.multiply(
    input1 = "00_base.tif",
    input2 = lc,
    output = "00_lc_float.tif"
)

# convert rds to float

wbt.multiply(
    input1 = "00_base.tif",
    input2 = rds,
    output = "00_rds_float.tif"
)

#  invert roads

wbt.reclass(
    i = "00_rds_float.tif",
    output = "01_rds_reclass.tif",
    reclass_vals = "1.0;0.0;0.0;1.0",
    assign_mode=True
)

# erase roads from land cover

wbt.multiply(
    input1 = "01_rds_reclass.tif",
    input2 = "00_lc_float.tif",
    output = "02_lc_multiply.tif"
)

# reclass roads binary to lc road value

wbt.reclass(
    i = "00_rds_float.tif",
    output = "11_rds_reclass.tif",
    reclass_vals = "0.0;0.0;6.0;1.0",
    assign_mode=True
)

# add lc road value to lc with roads erased

wbt.add(
    input1 = "11_rds_reclass.tif",
    input2 = "02_lc_multiply.tif",
    output = "21_lc_rds_add.tif"
)

# reclass lc values to friction (seconds for 5 pixel raster)

wbt.reclass(
    i = "21_lc_rds_add.tif",
    output = "23_friction.tif",
    reclass_vals = "5.59;1.0;5.59;2.0;0.25;3.0;5000.0;4.0;5000.0;5.0;0.25;6.0;2.24;7.0;5.59;8.0",
    assign_mode=True
)

# convert origin shapefile to raster

wbt.vector_points_to_raster(
    i = "origins.shp",
    output = "11_origins.tif",
    field="id",
    assign="first",
    nodata=True,
    cell_size=None,
    base="01_rds_reclass.tif"
)

wbt.cost_distance(
    source = "11_origins.tif",
    cost = "23_friction.tif",
    out_accum = "_24_accumulation.tif",
    out_backlink = "_24_backlink.tif"
)

#  alternative: simple friction from roads raster

wbt.reclass(
    i = "00_rds_float.tif",
    output = "z2_friction.tif",
    reclass_vals = "5.59;0.0;0.28;1.0",
    assign_mode=True
)

wbt.cost_distance(
    source = "11_origins.tif",
    cost = "z2_friction.tif",
    out_accum = "_z2_accumulation.tif",
    out_backlink = "_z2_backlink.tif"
)
