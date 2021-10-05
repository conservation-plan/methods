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

## 1. Replicate script  

Atom>File>New File 'shadedRelief.py' into project folder. Copy script from [methods repo](https://github.com/GEOG0310/methods/tree/master/wbHome){target=_blank}. Paste script into 'shadedRelief.py'. Save file.    

## 2. Organize workspace     

Make a 'data' directory within your 'wbt_pySpace' directory (if you do not already have one).

Copy the path to 'data' folder so you can set it as the working directory.  

```python
wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/methods/wbt_pySpace/data"
```

Also check the name for your DEM (it may not be the same as below).

```python
dem = "../testDEM/_02_testLidar.tif"
```  

## 3. Run  script  

In Atom, packages>script>run script. (Short cut: Command-I on Mac or Control-I on Windows).    

## 4. Inspect result  

In Q, add the layer and change the symbology to a red ramp. It should look like picture below.  

![result](../images/wbt_slopeClass/result.png)
