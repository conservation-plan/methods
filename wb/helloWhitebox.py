# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/testData"

# Declare a name for our test data

dem = "test_dsm.tif"

# Call the slope tool and define parameters

wbt.slope(
    dem = dem,
    output = "_test_slope.tif",
    zfactor=None,
    units="degrees"
)
