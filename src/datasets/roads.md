## Source  

[**VT Data - E911 Road Centerlines**](https://geodata.vermont.gov/datasets/vt-data-e911-road-centerlines-1/explore){target=_blank}

_Accessed 11/2021_  

## Process

With Earth Engine:  

1. Load data from asset id and filter by a region (we used Addison County).  
2. Convert roads to raster with 'AOTCLASS' raster values   
3. Create layers for the following classes of roads:  
    - Class 3   
    - Class 4  
    - State Forest Highway  
    - National Forest Highway  
    - Legal trail  
    - Private road  
    - Ferry  
4. Create layer for all State and Federal highways or interstates as all roads that are not one of the above classes.  
5. Create layer for **Fragmenting Roads** as all State or Federal highways or Class 3 roads.   

## EE snippet  

```js
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  Roads from VTrans
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var roads = ee.FeatureCollection('projects/conservation-atlas/assets/infrastructure/e911_road_centerlines')
  .filterBounds(region);

print("Roads", roads.first(), tool.tokenList(roads, "AOTCLASS"));

//  Rasterize roads by aot class
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var rdsImage = tool.makeImageFromFeatures(roads, 'AOTCLASS');


var rds3 = rdsImage.eq(3);            //  Class 3 Town Roads
var rds4 = rdsImage.eq(4);            //  Class 4 Town Roads
var rdsSFH = rdsImage.eq(5);          //  State Forest Highway
var rdsNFH = rdsImage.eq(6);          //  National Forest Highway
var rdsTrail = rdsImage.eq(7);        //  Legal trails
var rdsPrivate = rdsImage.eq(9);      //  Private Road
var rdsFerry = rdsImage.eq(65);       //  Ferry

var rdsHighways = rdsImage
  .gte(1)
  .subtract(rds3)
  .subtract(rds4)
  .subtract(rdsTrail)
  .subtract(rdsPrivate)
  .subtract(rdsFerry)
  .subtract(rdsSFH)
  .subtract(rdsNFH);

var rdsFragmenting = rdsHighways
  .add(rds3)
  .gte(1);

```  

## Dependencies  

The roads dataset is statewide, so the snippet above filters the dataset by a study region (Addison County).   

```js
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  Define study extent
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var region = ee.FeatureCollection("TIGER/2018/Counties")
  .filter(ee.Filter.eq('NAME', 'Addison'));
```

## Visualize

Each layer is a binary, where the value 1 represents 'roads' and the value 0 represents 'not roads'. The 'not road' locations can be masked when added as a layer.

```js
Map.addLayer(rds3.selfMask(), {palette: ["White"]}, "Class 3 Town Roads", 0, 1);
Map.addLayer(rds4.selfMask(), {palette: ["#00B3A6"]}, "Class 4 Town Roads", 0, 1);
Map.addLayer(rdsSFH.selfMask(), {palette: ["#00B3A6"]}, "State Forest Highwway", 0, 1);
Map.addLayer(rdsNFH.selfMask(), {palette: ["#00B3A6"]}, "National Forest Highway", 0, 1);
Map.addLayer(rdsTrail.eq(7).selfMask(), {palette: ["#00B3A6"]}, "Legal Trail", 0, 1);
Map.addLayer(rdsPrivate.eq(9).selfMask(), {palette: ["#00B3A6"]}, "Private Road", 0, 1);
Map.addLayer(rdsFerry.eq(65).selfMask(), {palette: ["#00B3A6"]}, "Ferry", 0, 1);
Map.addLayer(rdsHighways.selfMask(), {palette: ['#B34712']}, "Highways",0,1);
```

## Known issues  

In Middlebury, the dataset omits South Ridge Drive and does not show related closures to Middle Road.   
