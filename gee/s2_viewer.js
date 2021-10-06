//  --------------------------------------------------------------------------------
//  Name:    s2_viewer.js
//  Purpose: Find Sentinel 2 imagery, compare two images and color schemes, export clip
//
//  Author:  Jeff Howarth
//  Created: 10/06/2021
//  License: Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
//  --------------------------------------------------------------------------------

//  IMPORT MODULE
//  This gives you access to a set of FUNCTIONS I have written
//  to help you carry out some common tasks without getting bogged down in code.

var geoTools = require('users/jhowarth/conservation:modules/geoTools.js');

//  --------------------------------------------------------------------------------
//  STEP 1:
//  DEFINE YOUR STUDY REGION EXTENT
//
//  The starter script below defines the extent by a county boundary
//  (Addison County, Vermont).
//
//  --------------------------------------------------------------------------------

//  This loads a county in the USA
//  Example below selects Addison County, Vermont

var extent = ee.FeatureCollection("TIGER/2018/Counties")  //  County feature collection
  .filter(ee.Filter.eq('STATEFP', '50'))                  //  State code
  .filter(ee.Filter.eq('NAME', 'Addison'))                //  County name
  .geometry()                                             //  Returns geometry of feature
  ;

//  --------------------------------------------------------------------------------
//  STEP 2:
//  PRINT LIST OF DATES AVAILABLE BASED ON EXTENT AND CLOUD PERCENTAGE
//
//  The function 's2DatesList() takes two arguments:
//    extent: you just defined this in the last step
//    percent: the maximum percent cover of clouds in the image to filter
//  --------------------------------------------------------------------------------

//  You will not need to change the extent parameter, unless you changed the name above
//  You can adjust the cloud percentage. The default is 10% cloud coverage maximum.

var listdates = geoTools.s2DatesList(extent, 10);

//  --------------------------------------------------------------------------------
//  STEP 3:
//  CUSTOMIZE VIZ PARAMETERS FOR LEFT AND RIGHT MAPS
//
//  - color scheme options are listed below
//  - define the color scheme for the BANDS key in the VIZ object
//  - to change contrast, customize the MIN, MAX, and GAMMA parameters
//  --------------------------------------------------------------------------------
//
//  Color scheme options

var natColor = ['B4','B3','B2'];                      //  Natural Colors
var falseColor = ['B8','B4','B3'];                    //  False color Infrared
var falseUrband = ['B12', 'B11', 'B4'];               //  False color Urban
var ag = ['B11', 'B8', 'B2'];                         //  Agriculture
var atPen = ['B12','B11','B8a'];                      //  atmospheric penetration
var healthVeg = ['B8','B11','B2'];                    //  Healthy vegetation
var landWater = ['B8','B11','B4'];                    //  Land/Water
var natColorAR = ['B12','B8','B3'];                   //  Natural Colors with Atmospheric Removal
var swir = ['B12','B8','B4'];                         //  Shortwave Infrared
var veg = ['B11','B8','B4'];                          //  Vegetation Analysis

//  --------------------------------------------------------------------------------

//  VIZ objects for left and right maps

var leftViz = {
  min: 0.0,             //  CHOOSE min data value to increase or decrease contrast
  max: 0.3,             //  CHOOSE max data value to increase or decrease contrast
  gamma: 1.4,           //  CHOOSE gamma to increase or decrease contrast
  bands: natColor};     //  CHOOSE the color scheme from options above

var rightViz = {
  min: 0.0,             //  CHOOSE min data value to increase or decrease contrast
  max: 0.3,             //  CHOOSE max data value to increase or decrease contrast
  gamma: 1.4,           //  CHOOSE gamma to increase or decrease contrast
  bands: natColor};     //  CHOOSE the color scheme from options above

//  --------------------------------------------------------------------------------
//  STEP 4:
//  CHOOSE START AND END DATES FOR LEFT AND RIGHT MAPS
//
//  - the available dates should be printed to console from last step
//  - date format must be 'YYYY-MM-DD'
//  - date type must be a string (enclosed in single or double quotes)
//  - the start and end dates should be separated by a comma


var left = {
  start: '2019-06-01',  //  CHOOSE a start date
  end: '2019-08-01',    //  CHOOSE an End date
  cloud: 10,            //  CHOOSE max percent of image covered by clouds
  viz: leftViz,         //  Do not change this
};

var right = {
  start: '2020-03-01',  //  CHOOSE start date
  end: '2020-05-01',    //  CHOOSE end date
  cloud: 10,            //  CHOOSE max percent of image covered by clouds
  viz: rightViz         //  Do not change this
};

//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  AUTONOMOUS ZONE
//  You should not need to change anything in this section.
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

//  Construct images based on start, end, and cloud percentage
var leftImage = geoTools.sentinelImage(left.start, left.end,extent, left.cloud);
var rightImage = geoTools.sentinelImage(right.start, right.end,extent, right.cloud);

//  Configure layout
var leftMap = ui.Map();                               //  make left map
var rightMap = ui.Map();                              //  make right map
geoTools.makeSwipe(leftMap, rightMap);                //  make swipe layout

//  Compose layout
leftMap.centerObject(extent, 12);                     //  set center and zoom level
leftMap.setOptions('SATELLITE');                      //  left map base layer
rightMap.setOptions('HYBRID');                        //  right map base layer
leftMap.addLayer(leftImage.median(), leftViz, left.start,1,1);
rightMap.addLayer(rightImage.median(), rightViz, right.start,1,1);

//  ---------------------------------------------------------------------------------
//  STEP 5:
//  EXPORT IMAGE TO GOOGLE DRIVE
//  ---------------------------------------------------------------------------------

//  Google restricts how many pixels you can export.
//  The upper limit is 1e13.
//  Your two levers for meeting this limit are:
//    1. Limit the extent to a subregion
//    2. Increase the scale

//  ---------------------------------------------------------------------------------

//  DEFINE A CLIP REGION
//  The clipRegion below uses the extent of our testDEM to define a polyon to cli[ exports.
//  For projects, you will need to replace this with a clipRegion based on our study site.

var clipRegion = ee.FeatureCollection('users/jhowarth/geog0310/_testExtent').first().geometry();

//  DEFINE EXPORT PARAMETERS
//  The example below is set to export the LEFT IMAGE

var ex = {
  image: leftImage,         //  Choose if you want to export left or right mosaic image
  label: '_s2Export',        //  Choose image name
  scale: 10,                //  Choose the scale to export
  folder: 'EExport',        //  Choose folder on Google Drive to store the export
  CRS: 'EPSG:32145',        //  Choose coordinate reference system
  region: clipRegion,       //  Choose a region to clip export image
  viz: leftViz              //  Choose viz paramters for export image
  };

//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  AUTONOMOUS ZONE
//  You should not need to change anything in this section.
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var s2_export = ex.image                          //  Use image from export parameters
  .median()                                       //  Reduce overlapping values by median value
  .reproject(ex.CRS,null,ex.scale).resample()     //  Reproject to match study region CRS
  .visualize(ex.viz);                             //  Create RGB composite with viz object

var exportDict = {                                //  EXPORT PARAMETERS
  image: s2_export,                               //  Image to export
  description: ex.label,                          //  Name of task
  folder: ex.folder,                              //  Drive folder to store file
  fileNamePrefix: ex.label,                       //  Name of file
  region: ex.region,                              //  Clip export to this region
  scale: ex.scale,                                //  Export image at this resolution
  maxPixels: 1e13,                                //  Max pixels allowed by Google
  fileFormat: 'GeoTiff'                           //  Format of exported file
};

Export.image.toDrive(exportDict);                 //  EXECUTE EXPORT
