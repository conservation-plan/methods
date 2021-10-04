# -----------------------------------------------------------------------------
# Name:         heatLoadIndex.py
# Purpose:      Heat Load Index
#
# Author:       Jeff Howarth
# Created:      10/03/2021
# License:      Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#
# -----------------------------------------------------------------------------
# Parents:
#
# Evans, J. and Oakleaf J. (2014):
#   https://github.com/jeffreyevans/GradientMetrics/blob/master/scripts/hli.py
#   Accessed 10/03/2021
#
# Evans, J.:
#   https://rdrr.io/cran/spatialEco/src/R/hli.R
#   Accessed 10/03/2021
#
# -----------------------------------------------------------------------------
#
# References:
#
# McCune, B., and D. Keon (2002) Equations for potential annual
#   direct incident radiation and heat load index. Journal of
#   Vegetation Science. 13:603-606.
#
# McCune, B. (2007). Improved estimates of incident radiation and heat
#   load using non-parametric regression against topographic variables.
#   Journal of Vegetation Science 18:751-754.
# -----------------------------------------------------------------------------

# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# import math module
import math

# declare a name for the tools

wbt = WhiteboxTools()

# Define the Whitebox working directory
# You will need to change the path below to your local path name

wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/reland-tools/wbHome/data"

# turn off verbose mode
#wbt.verbose = False

# Declare a name for our test data

dem = "../testDEM/_02_testLidar.tif"

## model
## --------------------------------------

# l = latitude in radians for Midd = 0.7681732261
# cl = cosine of l = 0.7191811527
# sl = sine of l = 0.6948226173

l = 44.01308258 # latitude for Middlebury, Vermont
lr = l * 0.017453293 # latitude in radians
cl = math.cos(lr)
sl = math.sin(lr)

# tmp1 = slope in radians
wbt.slope(dem,"tmp1.tif",None,"radians")

# tmp2 = aspect in radians
wbt.aspect(dem,"aspect.tif",None)
wbt.multiply("aspect.tif",0.017453293,"tmp2.tif")

# tmp3
wbt.subtract("tmp2.tif", 3.926991,"tmp3a.tif")
wbt.absolute_value("tmp3a.tif","tmp3b.tif")
wbt.subtract(3.141593, "tmp3b.tif","tmp3c.tif")
wbt.absolute_value("tmp3c.tif","tmp3.tif")

# tmp4
wbt.cos("tmp1.tif","tmp4.tif")

#tmp5
wbt.sin("tmp1.tif","tmp5.tif")

# tmp6
wbt.cos("tmp3.tif","tmp6.tif")

#tmp7
wbt.sin("tmp3.tif","tmp7.tif")

#output raster

# clause A
a1 = 1.582 * cl
wbt.multiply(a1, "tmp4.tif", "A.tif")

# clause B
b1 = 1.5 * sl
wbt.multiply(b1, "tmp6.tif", "B1.tif")
wbt.multiply("B1.tif", "tmp5.tif", "B.tif")

# clause C
c1 = 0.262 * sl
wbt.multiply(c1, "tmp5.tif", "C.tif")

# clause D
wbt.multiply(0.607, "tmp7.tif", "D1.tif")
wbt.multiply("D1.tif", "tmp5.tif", "D.tif")

# combination
wbt.add(-1.467, "A.tif", "z1.tif")
wbt.subtract("z1.tif", "B.tif","z2.tif")
wbt.subtract("z2.tif", "C.tif","z3.tif")
wbt.add("z3.tif", "D.tif", "z4.tif")
wbt.exp("z4.tif", "_hli.tif")
