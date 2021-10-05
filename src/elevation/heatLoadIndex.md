## Purpose  

The heatLoadIndex tool produces a heat load index layer from a DEM.  

## Background  

*Need discussion of climate change refugia. Reference this [review article](https://drive.google.com/file/d/1XnwXB7ciCYwoatmLcbT7yjwTtmFtVucw/view?usp=sharing){target=_blank} and this [methods article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0143619){target=_blank}.*

## 1. Replicate script  

Atom>File>New File 'shadedRelief.py' into project folder. Copy script from [methods repo](https://github.com/GEOG0310/methods/tree/master/wbHome){target=_blank}. Paste script into 'shadedRelief.py'. Save file.    

## 2. Organize workspace     

Make a 'data' directory within your 'wbt_pySpace' directory (if you do not already have one).

Copy the path to 'data' folder so you can set it as the working directory.  

```python
wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/methods/wbHome/data"
```

Also check the name for your DEM (it may not be the same as below).

```python
dem = "../testDEM/_02_testLidar.tif"
```  

## 3. Run  script  

In Atom, packages>script>run script. (Short cut: Command-I on Mac or Control-I on Windows).   

## 4. Inspect result  

In Q, add the layer to a project.   

![result](../images/wbt_hli/result.png)

## 5. Style your layer

In Q, change symbology to display layer with three classes that follow Theobald article.    
