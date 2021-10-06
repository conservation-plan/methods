## Select tiles by extent  

1. Using extent of area and index of tiles, select tiles that intersect extent.
2. Field calculator  
    - Create new field  
        - Name: imgPath
        - Type: Text  
        - Length: 150
        - Expression:  
```
 '/Volumes/LaCie/data/vtRasters/vtLidar' + right( "DOWNLOAD_P" , length( "DOWNLOAD_P" ) - 6)
```

3. Field calculator
    - Create new field  
        - Name: year    
        - Type: integer  
        - Length: 4
        - Expression:
```
right(left( "DOWNLOAD_P" , 57),4)  
```

4. Export features
    - Format: CSV
    - File Name: lidarList.csv
    - Encoding: UTF-8
    - Select fields: 'imgPath' only
    - Geometry: 'no geometry'  

5. Open csv in text editor>remove first row ('imgPath' field name)
    - note: also need to sort list here so more recent files are on bottom of list. This will all

## Build virtual raster  

```
gdalbuildvrt -resolution average -r bilinear -allow_projection_difference -input_file_list '/Volumes/LaCie/projects/ocWetlands/lidarTileExtent/lidarList.csv' '/Volumes/LaCie/projects/ocWetlands/ocwElevation/ocwDEM.vrt'
```

## Translate raster  

```
gdal_translate -ot Float32 -of GTiff -r nearest '/Volumes/LaCie/projects/ocWetlands/ocwElevation/ocwDEM.vrt' '/Volumes/LaCie/projects/ocWetlands/ocwElevation/ocwDEM_mosaic.tif'
```
