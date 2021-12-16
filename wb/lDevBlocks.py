#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:     lDevBlocks.py
#  purpose:  to identify blocks of developed land
#
#  author:   Jeff Howarth
#  update:   12/15/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

# Full data
wbt.work_dir = "/Volumes/LaCie/plans/methods/wb/data/lDevBlocks"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Full datasets

rds = "/Volumes/LaCie/plans/methods/wb/data/midd/rdsFragmenting_12092021.tif"        # Highways and Class 3 roads
lc = "/Volumes/LaCie/plans/methods/wb/data/midd/iLandCover_midd_12152021.tif"              # 2016 Vermont base land cover
res = "/Volumes/LaCie/plans/methods/wb/data/midd/fE911ResPtsVtsp.shp"
trees = "/Volumes/LaCie/plans/methods/wb/data/midd/treeBinary_12122021.tif"

# Test datasets

# rds = "rds_fragmenting.tif"       # Highways and Class 3 roads
# bb = "buildingsBuffer100ft.tif"   # 2016 building footprints with 100 ft buffer
# lc = "lc_5m.tif"                  # 2016 Vermont base land cover

cRule = False        # Clump rule (no diagonals)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 1:
# Define target block type
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Isolate target

# Developed space

wbt.reclass(
    i = lc,
    output = "11_developed.tif",
    reclass_vals = "0;0;0;1;0;2;0;3;0;4;1;5;1;6;1;7;0;8;1;9;0;10",
    assign_mode=True
)

target = "11_developed.tif"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 2:
# Filter and lump targets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Remove small isolated pixels (usually from bare ground along roads, etc)

wbt.majority_filter(
    i = "11_developed.tif",
    output = "21_devMajFilter",
    filterx=21,
    filtery=21
)

# Identify contiguous patches

wbt.clump(
    i = "21_devMajFilter.tif",
    output = "22_developedClumps.tif",
    diag=cRule,
    zero_back=True
)

# Set background value

wbt.set_nodata_value(
    i = "22_developedClumps.tif",
    output = "23_devClumps_nd0.tif",
    back_value=0.0
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 3:
# Define area classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Compute area of clumps

wbt.raster_area(
    i = "23_devClumps_nd0.tif",
    output= "31_devClumpsArea.tif",
    out_text=False,
    units="map units",
    zero_back=True
)

# Convert to acres

wbt.divide(
    input1 = "31_devClumpsArea.tif",
    input2 = 4046.86,
    output = "32_devClumpAreaAcres.tif",
)

# Reclass area on log scale

wbt.quantiles(
    i = "32_devClumpAreaAcres.tif",
    output = "33_devAreaQuantiles.tif",
    num_quantiles=4
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 4:
# Define residential density classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wbt.vector_points_to_raster(
    i = res,
    output = "41_resPts.tif",
    field="TAG",
    assign="last",
    nodata=True,
    base=lc
)

wbt.reclass(
    i = "41_resPts.tif",
    output = "41_resReclass.tif",
    reclass_vals = "0;0;1;1;1;2;1;3;1;4;1;5;1;6;1;7;1;8",
    assign_mode=True
)

wbt.zonal_statistics(
    i = "41_resReclass.tif",
    features = "23_devClumps_nd0.tif",
    output= "42_resTotal.tif",
    stat="sum",
    out_table=None
)

wbt.new_raster_from_base(
    base = lc,
    output = "43_constantRaster.tif",
    value=1,
    data_type="float"
)

wbt.zonal_statistics(
    i = "43_constantRaster.tif",
    features = "23_devClumps_nd0.tif",
    output= "44_clumpTotal.tif",
    stat="sum",
    out_table=None
)

wbt.divide(
    input1 = "42_resTotal.tif",
    input2 = "44_clumpTotal.tif",
    output = "45_resDensity.tif"
)

wbt.quantiles(
    i = "45_resDensity.tif",
    output = "46_resDensityQuantiles.tif",
    num_quantiles=4
)
