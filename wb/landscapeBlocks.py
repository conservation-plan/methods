# import tools from WBT module

from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = '/Volumes/LaCie/GEOG0310/wbt_pySpace/lBlocks/data'

# Declare a name for our test data

lc = "/Volumes/LaCie/GEOG0310/wbt_pySpace/middData/iLandCover_midd_12092021.tif"

# Call the slope tool and define parameters

wbt.reclass(
    i = lc,
    output = '01_blocks.tif',
    reclass_vals = '1;0;1;1;2;2;3;3;2;4;4;5;4;6',
    assign_mode=False,
    callback=default_callback
)
