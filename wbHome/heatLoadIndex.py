# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/proLand-tools/outputs"

# Declare a name for our test data

dem = "../inputs/test_dsm.tif"

# Call the slope tool and define parameters

wbt.slope(
    dem = dem,
    output = "test_slope.tif",
    zfactor=None,
    units="degrees"
)
