## Data source        

In 1971, the Soil Conservation Service of the US Department of Agriculture published a [soil survey of Addison County](https://drive.google.com/file/d/1GN9uxFkiAravmXoiPGv27FQ4R3SmkQWI/view?usp=sharing){target=_blank}.

We used a shapefile of the soil map accessed from the [USDA Natural Resources Conservation Service Geospatial Data Gateway](https://datagateway.nrcs.usda.gov/){target=_blank} on Jan 2, 2021.

## Known problems  

Based on field work between 1941 and 1964, the Addison County soil survey relies on some of the oldest soil mapping in the state. As a result, the soil map reflects the knowledge and technology at this time. Surveys conducted later in the state describe some soil series that were not yet recognized at the time of the Addison County survey. Additionally, the boundaries of features on the soil map were produced by manually by transferring lines drawn on air photographs to a digital map layer. As a result, they should be interpreted as suggestive.  

The soil map was produced for the purpose of helping manage farms and woodlands, select sites for roads, ponds, buildings, and other structures, and evaluate the suitability of land for different land uses, such as agriculture, industry, and recreation. As a result, soils without much value for farming were not described in detail. For example, large swamps are mapped simply as 'muck and peat', while large areas of the Green Mountains are described as 'Rock Land.'  

## Key terms  

- **profile**: sequence of natural layers, or horizons, from the surface down to the parent material.  
- **soil series**: soils with similar profile, or with horizons of similar thickness, arrangement, and other important characteristics.   
- **soil phase**: soils of the same series with a differing quality that affects use of the soil by people, such as texture of the surface, slope, or stoniness.  
- **mapping unit**: the areas shown on a map (e.g. polygons), often corresponding roughly with soil phase.  
- **soil complex**: two or more soil series that are too small to distinguish and are instead listed as a compound joined with a hyphen (e.g. Nassau-Dutchess).  
- **undifferentiated group**: two or more soil series that could be delineated separately but are not necessary to separate for the purposes of the survey. These are listed with the conjunction 'and'.  
- **land types**: soils are so rocky, shallow, or severely eroded that they cannot be classified (e.g. "Rock land").  
- **soil associations**: a landscape that has distinctive proportional pattern of soils, normally consisting of one or more major soils at at least one minor soil.    

## Useful fields      

In 2016, the USDA Natural Resources Conservation Service (formerly SCS) updated a [**TOP20 table**](https://docs.google.com/document/d/1LPT5FhB2-0dhugBLNnevv6bnTyb0r5ZD/edit?usp=sharing&ouid=111896163379404259581&rtpof=true&sd=true){target=_blank} that tags map units with attributes for categories commonly used in land analysis. The following fields are contained in the shapefile's attribute table.    

| Category | Classes |
| :--- | :--- |
| AGVAL | Important Farmland Rating based on ["Farmland Classification System for Vermont Soils"](https://drive.google.com/file/d/1TP2_-SwG4UpUWVKo6tFRm49J1RJTLzhf/view?usp=sharing){target=_blank} |
| FLOOD | Flood frequency |
| FORSTGRP | Vermont forest land value groups |
| FORSTVAL | Relative forest value, based on ["Soil Potential Study and Forest Land Value Groups for Vermont Soils"](https://drive.google.com/file/d/1FIYQqlATksQmgdbP-QYz01jxDGlqLhpA/view?usp=sharing){target=_blank} |
| FROSTACTION | Potential frost action |
| GRAVEL | Potential source of gravel |
| HELCLASS | Erosion indexes from Universal Soil Loss Equation |  
| **HYDRIC** | Potential that hydric soils are present |  
| HYDROGROUP | Hydrological group - well-drained to poorly-drained |
| ONSITE | Onsite sewage disposal class |
| PARENT | General class of parent material |
| PARENTSUB | More detailed parent material class |  
| **PRIME** | Prime, Statewide, Local, NPSL, Not rated |
| ROCKSHALLOW <br>ROCKDEEP| Range in depth to bedrock (inches) |
| SAND | Potential for source of sand |  
| SLOPELOW <br> SLOPEHIGH | Range in slope (percent) |
| WATERSHALLOW <br>WATERDEEP | Range in depth to seasonal high water table  |
| WATERKIND | type of seasonal high water table: apparent or perched |
| KfactWS | Dominant condition soil erodibility factor for use in soil loss equations |
| TFACTOR | Tolerable soil loss for us in soil loss equations |   
