#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:     habitatBlocks.py
#  purpose:  to identify habitat blocks for conservation planning
#
#  author:   Jeff Howarth
#  update:   11/09/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

# Full data
wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/hb_midd"

# Test data
# wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/hb_test"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Full datasets

rds = "rdsFrag_0p5m.tif"        # Highways and Class 3 roads
bb = "bb_merge.tif"             # 2016 building footprints with 100 ft buffer
lc = "lc_0p5m.tif"              # 2016 Vermont base land cover

# Test datasets

# rds = "rds_fragmenting.tif"       # Highways and Class 3 roads
# bb = "buildingsBuffer100ft.tif"   # 2016 building footprints with 100 ft buffer
# lc = "lc_5m.tif"                  # 2016 Vermont base land cover

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 1:
# Create fragmentation layer from buildings and roads
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# buffer roads by 3 meters

wbt.buffer_raster(
    i = rds,
    output = "00_rds_buff3m.tif",
    size = 3,
    gridcells=False
)

# Add impervious land cover and buffered building together as constraints

wbt.add(
    input1 = "00_rds_buff3m.tif",
    input2 = bb,
    output = "01_constraints.tif"
)

# Make all constraints 0 and non constraints 1

wbt.reclass(
    i = "01_constraints.tif",
    output = "02_constraintsInverted.tif",
    reclass_vals = "1;0;1;0;1;99",
    assign_mode=False
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 2:
# Isolate tree canopy and lump small strips (from powerlines)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Isolate tree canopy

wbt.reclass(
    i = lc,
    output = "11_treeCanopy.tif",
    reclass_vals = "1;1;0;2;0;3;0;4;0;5;0;6;0;7;0;8",
    assign_mode=True
)

# buffer out 7.5 meters (to remove powerline cuts from forest)

wbt.buffer_raster(
    i = "11_treeCanopy.tif",
    output = "12_treeCanopyBuffered.tif",
    size = 7.5,
    gridcells=False
)

# invert the buffer

wbt.reclass(
    i = "12_treeCanopyBuffered.tif",
    output = "13_tcbInvert.tif",
    reclass_vals = "1;0;0;1",
    assign_mode=True
)

# buffer back in

wbt.buffer_raster(
    i = "13_tcbInvert.tif",
    output = "14_tcbInvertBuffered.tif",
    size = 7.5,
    gridcells=False
)

# invert back

wbt.reclass(
    i = "14_tcbInvertBuffered.tif",
    output = "15_treeCanopyGood.tif",
    reclass_vals = "1;0;0;1",
    assign_mode=True
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 3:
# Fragment tree canopy and identify clumps > 10 acres
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Erase constraints from tree canopy clumps

wbt.multiply(
    input1 = "02_constraintsInverted.tif",
    input2 = "15_treeCanopyGood.tif",
    output = "21_treesAfterConstraints.tif",
)

# Find contiguous regions of habitat

wbt.clump(
    i = "21_treesAfterConstraints.tif",
    output = "22_treeClumps.tif",
    diag=False,
    zero_back=True
)

# Compute area of each clump

wbt.raster_area(
    i = "22_treeClumps.tif",
    output= "23_treeClumpAreas.tif",
    out_text=False,
    units="map units",
    zero_back=True
)

# threshold for habitat block > 10 acres
# 10 acres = 40468.6 square meters

wbt.reclass(
    i = "23_treeClumpAreas.tif",
    output = "24_treeGT10acres.tif",
    reclass_vals = "0;0;40467;1;40467;999999999999999999999",
    assign_mode=False
)

wbt.convert_nodata_to_zero(
    i = "24_treeGT10acres.tif",
    output = "25_bigTreeClumps_nd0.tif"
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 4:
# Fill holes within habitat blocks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# First invert big tree clump raster

wbt.reclass(
    i = "25_bigTreeClumps_nd0.tif",
    output = "31_bigTreeClumps_invert.tif",
    reclass_vals = "0;1;1;0",
    assign_mode=True
)

# Identify clumps of unforested land

wbt.clump(
    i = "31_bigTreeClumps_invert.tif",
    output = "32_holeClumps.tif",
    diag=False,
    zero_back=True
)

# Compute area

wbt.raster_area(
    i = "32_holeClumps.tif",
    output= "33_holeClumpAreas.tif",
    out_text=False,
    units="map units",
    zero_back=True
)

# Reclass holes < 250 acres

wbt.reclass(
    i = "33_holeClumpAreas.tif",
    output = "34_holeLT250acres.tif",
    reclass_vals = "1;0;1011714;0;1011714;99999999999999999999999",
    assign_mode=False
)

wbt.convert_nodata_to_zero(
    i = "34_holeLT250acres.tif",
    output = "35_holeClumpAreas_nd0.tif"
)

## Add filled holes to tree clumps

wbt.add(
    input1 = "25_bigTreeClumps_nd0.tif",
    input2 = "35_holeClumpAreas_nd0.tif",
    output = "36_block_holes_filled.tif"
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 5:
# Identify discrete habitat blocks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Identify habitat blocks

wbt.clump(
    i = "36_block_holes_filled.tif",
    output = "41_habitatBlocks.tif",
    diag=False,
    zero_back=True
)

wbt.set_nodata_value(
    i = "41_habitatBlocks.tif",
    output = "_habitatBlocks_nd",
    back_value = 0,
)
