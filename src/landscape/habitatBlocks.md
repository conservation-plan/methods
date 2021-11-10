## Purpose  

To identify habitat blocks as directed by [Act 171](https://anr.vermont.gov/Planning/Forest_Blocks_And_Habitat_Connectors){target=_blank}.  

## Data prep  

- [Land cover](../data/landcover.md): to identify tree canopy and impervious or bare land    
- [Roads](../data/roads.md): to identify highways or interstates or Class 3 roads  
- [Buildings](../data/buildings.md): to identify areas within 100ft of a building (to remove landscaped tree canopy near buildings)  
- Export each dataset for Middlebury Study Area (_need to include a description for this_)

## Data process    

Main steps with Whitebox:  

1. Create fragmentation layer from buildings and roads  
2. Isolate tree canopy and lump small strips (from powerlines)  
3. Fragment tree canopy and identify clumps > 10 acres  
4. Fill holes within habitat blocks  
5. Identify discrete habitat blocks  

Link to python script
