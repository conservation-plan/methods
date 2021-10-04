## Purpose  

The slopeClass tool produces a layer that distinguishes six categories of slope from nearly level to very steep.    

## Background    

The slope classification system is based on the [USDA Natural Resources Conservation Service](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/soils/ref/?cid=nrcs142p2_054252){target=_blank} (see Table 2-3).  

The table below defines classes based on lower limits for simple slopes. Slope units are percent.  

| Class | From | To |
|:--- | :---: |:---:|
|Nearly level | 0 | <1 |
|Gently sloping | 1 | <4 |
|Strongly sloping | 4 | <10 |
|Moderately steep | 10 | <20 |  
|Steep | 20 | <45 |
|Very steep | 45 | >45 |  

## 1. Get files      

Download 'slopeClass.py' and 'slopeClass.txt' from the [reland-tools/wbHome repo](https://github.com/GEOG0310/reland-tools/tree/master/wbHome){target=_blank}.

## 2. Organize workspace    

Put both files into your wbt_pySpace directory so that they sit with your 'helloWhitebox.py' file and your WBT folder.  

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

In Q, add the layer and change the symbology to a red ramp. It should look like picture below.  

![result](../images/wbt_slopeClass/result.png)
