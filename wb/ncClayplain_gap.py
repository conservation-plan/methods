# -----------------------------------------------------------------------------
# Natural Communities Evaluate Conservation Gaps
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
# You will need to change the path below to your local path name

#test directory
wbt.work_dir = "/Volumes/LaCie/GEOG0310/wbt_pySpace/ebbyData"
#midd directory
#wbt.work_dir = "/Volumes/EbbyEHD/GEOG310/wbt_pySpace-master/midd"

### Datsets ###
#test
ncSoils = "naturalCommunities.tif"
proLands = "protectedLand.tif"
trees = "treeCanopy.tif"
hb  = "habitatBlocks.tif"
sigNatCom = "imageSig.tif"
region = "imageRegion.tif"
buildings = "buildingsBuffer.tif"
rc = "RiperianCorridors.tif"

# full dataset
 # ncSoils =
 # proLands =
 # trees =
 # hb  =
 # sigNatCom =
 # region =
 # buildings =

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 1: Identify current forest for each natural community
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# clean up tree canopy
# #tree canopy [1=tree 0=no tree] Buildings[0=building buffer; 1=not]

wbt.multiply(
    input1 = trees,
    input2 = buildings,
    output = "01_treeCanopyClean.tif"
)
# #reclass natural Communities to combine wet and mesic clayplain
#
wbt.reclass(
    i = ncSoils,
    output = "ncSoilsReclass",
    reclass_vals = '0;0;1;1;2;2;3;3;3;4;4;5;5;6;0;7;0;8',   #new value;oldvalue
    assign_mode=True
)
#
# #identify forest in each nc
#
wbt.multiply(
    input1 = "ncSoilsReclass.tif" ,
    input2 = "01_treeCanopyClean.tif",
    output = "natSoilsTrees.tif"
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 2: Filter by habitat blocks
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reclass habitat habitatBlocks to binary
#
wbt.reclass(
    i = hb,
    output = "hbBinary.tif",
    reclass_vals = '0;0;1;1;1;99999999999999',   #new value;oldvalue
    assign_mode=False
)
#
# ### Erase all natural community pixels outside of habitat blocks
#
wbt.multiply(
    input1 = "natSoilsTrees.tif" ,
    input2 = "hbBinary.tif",
    output = "natComHB.tif"
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 3: Identify targets from historic extents
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# idenify protection goals

# This will calculate historic extent of each community

wbt.raster_area(
    i = "ncSoilsReclass.tif",
    output="ncSoilsArea.tif",
    out_text=False,
    units="map units",
    zero_back=False
)
# #convert m2 to acres
wbt.divide(
    input1 = "ncSoilsArea.tif",
    input2 = 4046.86,
    output = "ncSoilsAcre.tif"
)
# # min/max = area of each nc in acres
wbt.zonal_statistics(
    i = "ncSoilsAcre.tif",
    features = "ncSoilsReclass.tif",
    output=None,
    stat="maximum",
    out_table= 'Targets.html'
)
#

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 4: Compare targets to current protections
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Isolate protected lands without agricultural land cover
#
wbt.reclass(
    i = proLands,
    output = "forestProtections",
    reclass_vals = '0;0;0;1;1;2',   #new value;oldvalue
    assign_mode=True
)
# # return total pixels in forest protection for each natural community
#
wbt.zonal_statistics(
    i = "forestProtections.tif",
    features = "natComHB.tif",
    output=None,
    stat="total",
    out_table= True
)
#
wbt.reclass(
    i = proLands,
    output = "agProtections",
    reclass_vals = '0;0;1;1;0;2',   #new value;oldvalue
    assign_mode=True
)
# # #
wbt.zonal_statistics(
    i = "agProtections.tif",
    features = "natComHB.tif",
    output=None,
    stat="total",
    out_table= 'currentPro.html'
)


 # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 # Part 5: Compare current clayplain conservation to proposed conservation with habitat Blocks
 # and riparian corridors
 # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#current extent of Clayplain
wbt.zonal_statistics(
    i = "08_generalClayplainSoils.tif",
    features = "_clayplainForestCurrent.tif",
    output= None,
    stat="total",
    out_table= True
)

##Current forest protections for clayplain

wbt.reclass(
    i = proLands,
    output = "forestProtections.tif",
    reclass_vals = '0;0;0;1;1;2',   #new value;oldvalue
    assign_mode=True
)
#
wbt.multiply(
    input1 = "_clayplainForestCurrent.tif",
    input2 = "forestProtections.tif",
    output = "protectedClayplain.tif"
)

wbt.zonal_statistics(
    i = "_clayplainForestCurrent.tif",
    features = "protectedClayplain.tif",
    output= None,
    stat="total",
    out_table= True
)



wbt.reclass(
    i = rc,
    output = "rcReclass.tif",
    reclass_vals = '0;0;10;1',   #new value;oldvalue
    assign_mode=True
)
wbt.add(
    input1 = "hbBinary.tif",
    input2 = "rcReclass.tif" ,
    output = "proposedProtected.tif",
)

# 0 = neither
# 1 = hb only
# 10 = rc only
# 11 = both hb and rc


wbt.zonal_statistics(
    i = "_clayplainForestCurrent.tif",
    features = "proposedProtected.tif",
    output= None,
    stat="total",
    out_table= 'proPro.html'
)
