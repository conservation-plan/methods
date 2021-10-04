## Purpose  

The shadedRelief tool produces three layers that can be combined to make shaded relief maps.  

## 1. Get script  

Download 'shadedRelief.py' from the [reland-tools/wbHome repo](https://github.com/GEOG0310/reland-tools/tree/master/wbHome){target=_blank}.  

## 2. Organize workspace     

Put the python file into your wbt_pySpace directory so that it sits with your 'helloWhitebox.py' file and your WBT folder.

## 3. Edit the script  

With Atom, open the python file.  

You will need to alter the working directory path. I suggest that you make a 'data' directory within your 'wbt_pySpace' directory (if you do not already have one), then use that path as the working directory. (Replace the path shown below).    

```python
wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/reland-tools/wbHome/data"
```

Also check the name for your DEM (it may not be the same as below).

```python
dem = "../testDEM/_02_testLidar.tif"
```

*We will take a moment here to walk through how the script works*.  

## 4. Run the script  

In Atom, packages>script>run script. (Short cut: Command-I on Mac or Control-I on Windows).  

## 5. Inspect result  

In Q, create a new **group** and name it **shaded relief**. Then add the three layers to the group.  

![result](../images/wbt_shadedRelief/result.png)

## 6. Style your shaded relief  

In Q, use layer order, transparency, and Symbology>blended mode to create a shaded relief map that helps you interpret the terrain.  
