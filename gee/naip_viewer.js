//  --------------------------------------------------------------------------------
//  Name:    naip_viewer.js
//  Purpose: Find NAIP imagery, compare two images, and export clip
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

//  Load extent as a county in the USA
//  Example below selects Addison County, Vermont

var extent = ee.FeatureCollection("TIGER/2018/Counties")  // County feature collection
  .filter(ee.Filter.eq('STATEFP', '50'))                  // State code
  .filter(ee.Filter.eq('NAME', 'Addison'))                // County name
  .geometry()                                             // Returns geometry (polygon)
  ;

//  --------------------------------------------------------------------------------
//  STEP 2:
//  PRINT LIST OF YEARS AVAILABLE BASED ON EXTENT AND BAND DEPTH
//
//  The function 'naipYearList(extent, #bands) takes two arguments:
//    extent: you just defined in the last step
//    #bands: the band depth, or 3 for R,G,B and 4 for N,R,G,B
//  --------------------------------------------------------------------------------

var listYears = geoTools.naipYearList(extent, 4);

//  --------------------------------------------------------------------------------
//  STEP 3:
//  CHOOSE YEAR AND COLOR SCHEME FOR IMAGES
//
//  For left and right maps:
//
//  Choose a year based on the list of years available (printed to console).
//  Choose a VIZ style (either NATURAL or FALSE color.
//  --------------------------------------------------------------------------------

//  Color scheme options
//  --------------------------------------------------------------------------------

var natColor = {min: 0, max: 255, bands: ['R', 'G', 'B'], gamma: 1};       // Healthy vegetation looks green
var falseColor = {min: 0,max: 255, bands: ['N', 'R', 'G'], gamma: 1};      // Healthy vegetation looks red

var left = {
  year: 2012,
  viz: falseColor
};

var right = {
  year: 2018,
  viz: falseColor
};

//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  AUTONOMOUS ZONE
//  You should not need to change anything in this section.
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var leftMosaic = geoTools.yearMosaic(extent, left.year);      //  make left mosaic image
var rightMosaic = geoTools.yearMosaic(extent, right.year);    //  make right mosaic image

var leftMap = ui.Map();                               //  make left map
var rightMap = ui.Map();                              //  make right map
geoTools.makeSwipe(leftMap, rightMap);                //  make swipe layout


leftMap.centerObject(extent, 12);                     //  set center and zoom level
leftMap.setOptions('SATELLITE');                      //  left map base layer
rightMap.setOptions('HYBRID');                        //  right map base layer
leftMap.addLayer(leftMosaic, left.viz, String(left.year),1,1);      //add layer to left
rightMap.addLayer(rightMosaic, right.viz, String(right.year),1,1);  //add layer to right


//  ---------------------------------------------------------------------------------
//  STEP 4:
//  EXPORT IMAGE TO GOOGLE DRIVE
//  ---------------------------------------------------------------------------------

//  Google restricts how many pixels you can export.
//  The upper limit is 1e13.
//  Your two levers for meeting this limit are:
//    1. Limit the extent to a subregion
//    2. Increase the scale

//  ---------------------------------------------------------------------------------

var clipRegion = ee.FeatureCollection('users/jhowarth/geog0310/_testExtent').first().geometry();

var ex = {
  image: leftMosaic,        //  Choose if you want to export left or right mosaic image
  label: '_naipExport',      //  Choose image name
  scale: 1,                 //  Choose the scale to export
  folder: 'EExport',        //  Choose folder on Google Drive to store the export
  CRS: 'EPSG:32145',        //  Choose coordinate reference system
  region: clipRegion,
  viz: left.viz
  };

//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//  AUTONOMOUS ZONE
//  You should not need to change anything in this section.
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

var naipExportPrep = ex.image                     //  image to export
  .reproject(ex.CRS,null,ex.scale).resample()     //  Reproject to project CRS
  .visualize(ex.viz)                              //  Make RGB compoosite with viz object

var exportDict = {                                //  EXPORT PARAMETERS
  image: naipExportPrep,                          //  image prepped to export
  description: ex.label,                          //  task label
  folder: ex.folder,                              //  drive folder name
  fileNamePrefix: ex.label,                       //  file name
  region: ex.region,                              //  clip export to this extent
  scale: ex.scale,                                //  export image at this resolution
  maxPixels: 1e13,                                //  max pixels allowed by Google
  fileFormat: 'GeoTiff'                           //  export image in this format
};

Export.image.toDrive(exportDict);                 //  EXECUTE EXPORT
