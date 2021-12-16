# -----------------------------------------------------------------------------
# Natural Communities Present Conditions Workflow--- Clayplain
# REVIEWER: WILL BEHM
# REVIEW DATE: 12/6/21
# RUN STATUS: READY!
#SUPPORT STATUS: ALL CLEAR!
# -----------------------------------------------------------------------------

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Define the Whitebox working directory
#test Region
wbt.work_dir = "/Volumes/LaCie/GEOG0310/wbt_pySpace/ebbyData"

#total study site (Middlebury)
#wbt.work_dir = "/Volumes/EbbyEHD/GEOG310/wbt_pySpace-master/midd"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Test Region datasets

ncSoils = "naturalCommunities.tif"         # natural communties from soil #NOTE (WB)-> Changed name to naturalCommunities.tif here because it did not match the name from earth engine
buildings = "buildingsBuffer.tif"    # buildings with 100ft buffer
Ag = "AgImage.tif"                     #agricultural land
lc = "landCover.tif"                    #land cover data

# Full Datasets
# ncSoils =
# buildings =
# Ag =
# lc =

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 1: Distinguish agriculture and human landscaping from natural land cover
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#burn ag into land Cover

wbt.reclass(
    i = Ag,
    output = "01_agReclass",
    reclass_vals = '0;0;10;1',   #new value;oldvalue
    assign_mode=True
)

wbt.add(
    input1 = "01_agReclass.tif",
    input2 = lc,
    output = "02_landCoverwithAg.tif"
)

# Original landcover classes:
# 1: tree canopy
# 2: grass/shrub
# 3: bare soil (often quarries)
# 4: water
# 5: buildings
# 6: roads
# 7: other paved
# 8: railroads

wbt.reclass(
    i = "02_landCoverwithAg.tif",
    output = "03_reclassify.tif",
    reclass_vals = '1;1;2;2;4;3;5;4;4;5;4;6;4;7;4;8;3;11;3;12;3;13;3;14;3;15;3;16;3;17;3;18',   #new value;oldvalue;
    assign_mode=True
)

# Result:
# 0 = none
# 1 = tree canopy
# 2 = grass/shrublands
# 3 = ag
# 4 = developed (bare soils, buildings, roads, other paved surfaces, railroads)
# 5 = water

#burn buffered buildings into lc+Ag

wbt.reclass(
    i = buildings,
    output = "04_buildingsReclass.tif",
    reclass_vals = '10;0;0;1',   #new value;oldvalue
    assign_mode=True
)

wbt.add(
    input1 = "04_buildingsReclass.tif",
    input2 = "03_reclassify.tif",
    output = "05_lcWithBuildings.tif"
)

wbt.reclass(
    i = "05_lcWithBuildings.tif",
    output = "06_lcFinal.tif",
    reclass_vals = '1;1;2;2;3;3;4;4;5;5;4;10;4;11;4;12;4;13;4;14;4;15',   #new value;oldvalue
    assign_mode=True
)

# Result:
# 0 = water
# 1 = tree Canopy
# 2 = grass/shrublands
# 3 = ag
# 4 = developed (all developed from above plus land within 100ft of buildings
# 5 = water

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 2: Combine updated land cover with clayplain soils
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# isolate just clayplain soils

# Result:
# 1: wet clayplain
# 10: mesic clayplain
# 0: all other community types

wbt.reclass(
    i = ncSoils,
    output = "07_clayplainSoils.tif",
    reclass_vals = '0;0;0;1;0;2;1;3;10;4;0;5;0;6;0;7;0;8',   #new value;oldvalue
    assign_mode=True
)

# multiply updated landCover with Clayplain soils to identify which lc type are on clayplain soils

wbt.multiply(
    input1 = "06_lcFinal.tif",
    input2 = "07_clayplainSoils.tif",
    output = "_clayplainLandCover.tif"
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 3: Visualize current extent of clayplain forests in the region
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# isolate just current clayplain forests (places that are tree canopy and clayplain soils)

wbt.reclass(
    i = "_clayplainLandCover.tif",
    output = "_clayplainForestCurrent.tif",
    reclass_vals = '1;1;0;2;0;3;0;4;0;5;1;10;0;20;0;30;0;40;0;50',   #new value;oldvalue
    assign_mode=True
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 4: Calculate amount of change (total number of pixels)
#   from historic clayplain forest (based on soils)
#   to current land cover classes
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# isolate clayplain forest soils from other natural communities
# but without distinguishing between wet and mesic variants

wbt.reclass(
    i = ncSoils,
    output = "08_generalClayplainSoils.tif",
    reclass_vals = '0;0;0;1;0;2;1;3;1;4;0;5;0;6;0;7;0;8',   #new value;oldvalue
    assign_mode=True
)

# #
wbt.zonal_statistics(
    i = "08_generalClayplainSoils.tif",
    features = "_clayplainLandCover.tif",
    output="testCP.tif",
    stat="total",
    out_table= True
)
