## Source  

[**Vermont 3D Building Roofprints 2016**](https://geodata.vermont.gov/pages/land-cover){target=_blank}

_Accessed 10/2021_  

## Process  

With Earth Engine:  

1. Load buildings with asset ID and filter by study region.  
2. Buffer each building by 100 ft  
3. Rasterize building footprints  
4. Rasterize building footprints with 100 ft buffer  

## Snippet

```js
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  Buildings
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var buildings = ee.FeatureCollection('projects/conservation-atlas/assets/landCover/lcBuildings_2016')
  .filterBounds(region);

//  Function to buffer buildings by 100 feet
var makeBuffer = function(f) {
  return f.buffer(30.48);
};

//  Apply buffer function to each building in feature collection
var buildingBuffer = buildings.map(makeBuffer);

//  Rasterize building features
var buildBufferImage = tool.makeImageFromFeatures(buildingBuffer.map(tool.tag), 'TAG');
var imageBB = tool.makeImageFromFeatures(buildingBuffer.map(tool.tag), 'TAG');
var imageBB_inv = imageBB.unmask().lt(1);
```

## Dependencies  

The buildingsBuffer100ft dataset is statewide, so the snippet above filters the dataset by a study region (Addison County).   

```js
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  Define study extent
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var region = ee.FeatureCollection("TIGER/2018/Counties")
  .filter(ee.Filter.eq('NAME', 'Addison'));
```

## Known issues  

The source dataset was produced in 2016. Therefore, changes to the built environment after this date are not captured by the dataset. For example, the dataset shows the old barn at the Lussier Farm on Middlebury College lands.   
