## Source  

[**Vermont Base Land Cover 2016**](https://geodata.vermont.gov/pages/land-cover){target=_blank}

_Accessed 10/2021_  

## Process  

With Earth Engine:  

1. Load landcover with asset ID.  
2. Generalize classes as follows:  
    1. Tree canopy
    2. Grass/shrub  
    3. Water  
    4. Bare or impervious   
3. Create color palette for generalized land cover   
4. Create viz scheme for generalized land cover    

## Snippet

```js
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  Land Cover
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

//  Simplified land cover base
var lc = ee.Image('users/jhowarth/middCC/LandLandcov_BaseLC2016');

var lcSimple = lc.remap([1,2,3,4,5,6,7,8],[1,2,4,3,5,4,4,4]);

var lcP1 = ['#79DB8E','#99F291', '#89F9C1', 'white','#8F323D'];

var lcViz = {min:1, max:5, palette: lcP1};

```

## Dependencies  

None.

## Known issues  

The source dataset was produced in 2016. Therefore, changes to the environment after this date are not captured by the dataset.  
