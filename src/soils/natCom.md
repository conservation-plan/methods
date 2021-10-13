_WORK IN PROGRESS_  

Below, I've largely pasted the log that I kept while I processed the data. I have not yet finished revising this to make it more reader friendly.  

You can see an example of the dataset in this draft of a [conservation atlas](https://jhowarth.users.earthengine.app/view/conservation-planning){target=_blank} for Addison County.     

## Introduction  

This dataset uses geographic information from a [soil survey](survey.md) to create a map of potential natural communities.  

In 2005, Thomas Villars, a Soil Resource Specialist for the USDA Natural Resources Conservation Service, working with Elizabeth H. Thompson and Eric R. Sorenson, authors of *Wetland, Woodland, Wildland -- A Guide to the Natural Communities of Vermont*, wrote a [report](https://drive.google.com/file/d/1F6-iq5-Duq4ixJ3BVIbK1ADH_cQeC8uz/view?usp=sharing){target=_blank} and developed a [table](https://docs.google.com/spreadsheets/d/1fsoxPz7ssAm_IEVcve-pv4SX_GGQLF7w/edit?usp=sharing&ouid=111896163379404259581&rtpof=true&sd=true){target=_blank} that associates natural communities to soil series.  

### Schema plan

This is the goal, the dataset I'm trying to make, showing the schema.  

| Table | Purpose |  
| :---: | :--- |  
| nc | Natural community descriptions indexed by page |  
| ncf | Natural community formations indexed by page |  
| nct | Natural community types indexed by page |  
| add_ss | Soil series for Addison County |  
| add_sf | Soil features for Addison County |  

Hierarchy for natural communities  

- Type  
    - Formation  
        - Community  

Hierarchy for soils  

- Soil series  
    - Soil features  

Links between natural communities and soils  

-  1:many community links to features

### Check key codes for communities  

Villars lists the page number for each community. I'd like to use these as the keys for the communities, but the problem is that he lists variants for some communities and these variants have short descriptions so in a few cases the page numbers are not unique. For Addison County, there are three conflicts:

- 134 repeated twice
- 148 repeated twice
- 251 repeated twice  

I'd like the page data types to remain integer, so it seems like the easiest solution is to add a digit to the repeaters. (For example, 1341 and 1342). I'd then have to update the table that lists nat communities for each soil, which would be a bit of a hassle, but hopefully just a find and replace edit.  

Ah- here's the glitch with that. I have the right function set up to grab 3 characters, so I'd like the change to remain three digits. Since the descriptions start on page 82, I should be able to create new codes that are less than 100. Like this:

- 134a : 034  
- 134b : 134  
- 148a : 048  
- 148b : 148  
- 251a : 051  
- 251b : 251  

The cuts down on the number of find and replace steps I need to do too.  

### Clean up keys for Addison Soils and Villars table  

The main challenge here is that Villars names communities for each soil series, but the Addison survey lists a couple of series as complexes that combine two series.  

Here are the composites in the soil survey:  

  1. Berkshire-Marlow  
  2. Calais-Glover  
  3. Covington-Panton  
  4. Farmington-Nellis  
  5. Lyman-Berkshire  
  6. Nassau-Dutchess  

I can think of the following solutions:  

  1. Split the feature into two overlapping polygons  
  2. Conflate the attributes into a single row  

I'd rather not duplicate the polygons because this would complicate area estimations. So let's think through the aggregation.  

#### Berkshire-Marlow

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Berkshire | 132 | 142 | 034 |
| Marlow | 132 | 034 |
| Berkshire-Marlow | 132 | 142 | 034 |

This seems reasonable. Marlow is a subset of Berkshire.

#### Calais-Glover

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Calais | 132 | 138 | 134 |
| Glover | 132 | 142 | 169 | 138 |
| Calais-Glover | 132 | 138 | 142 | 134 | 169 |

This solution just alternates the list following the first one that they have in common. It at least lists all potential communities. All the communities are of the same formation, except for 169.  

#### Covington-Panton  

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Covington | 175 |  |  |
| Panton | 175 | 174 |
| Covington-Panton | 175 | 174 |  |  |  |

In this solution, the first community is shared and the second community is inherited from the Panton soil.  

#### Farmington-Nellis  

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Farmington | 171 | 172 | 160 | | 139 |
| Nellis | 171 | 138 | 134 |
| Farmington-Nellis| 171 | 172 | 138 | 160 | 134 | 139 |

This solution follows the alternating pattern. The main concern here is that the communities span more than one formation. At least they both share a common first community in the same formation. These soils both formed in glacial till in the valley.

#### Lyman-Berkshire

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Lyman | 048 | 132 | 142 | |  |
| Berkshire | 132 | 142 | 034 |
| Lyman-Berkshire| 148 | 132 | 142 | 034 |  |  |

Since the hyphenation is not alphabetical, I assume it represents dominance. So I start with the Lyman nat community. They share two communities. The last community is unique to Berkshire, but it is a variant of something they have in common. All communities are of the same formation.  


#### Nassau-Dutchess

| soil_series | nc1 | nc2 | nc3 | nc4| nc5 | nc 6 |
|:---| :---: | :---: | :---: | :---: | :---: | :---: |
| Nassau | 163 | 171 |  | |  |
| Dutchess | 171 | 142 |  |
| Nassau-Dutchess| 163 | 171 | 142 |  |  |  |

Again, not alphabetical so I assume ordinal dominance. They share one community. Note that the second community for Dutchess is a different formation.  

### Non-soil types in NRCS survey  

The soil survey describes a handful of features that do not map directly to Villars table.

**Solution:** repeat the soil description as the nat_com1 description and then link to a formation code to generalize with other features. For Muck, type is Forested Wetland (244). For Marsh, type is Open or Shrub Wetlands (309). For others, type codes are new and identify Hydrological features, Undescribed rocky lands, Mining lands.

| cpage | community | fpage | nat_form | type | tpage | skey |    
| :---:| --- | :--- | :---: | :---: | :---: |:---: |
| 510 | Muck and Peat | 500 | Swamp | 244 | Forested Wetlands | Muck |
| 610 | Fresh water marsh | 600 | Marsh | 309 | Open or Shrub Wetlands | Fresh |
| 710 | Cobbly allivial land | 700 | Hydrology | 700 | Hydrological Features | Cobbly |
| 720 | Water | 700 | Hydrology | 700 | Hydrological Features | Water |
| 810 | Rock land  | 800 | Rocky lands | 800  | Undescribed rocky lands | Rock |
| 820 | Rubble land | 800 | Rocky lands | 800 | Undescribed rocky lands | Rubble |
| 910 | Gravel pits | 900 | Mine | 900 | Mining Lands | Gravel |
| 920 | Quarry  | 900 | Mine | 900 | Mining lands | Quarry |

### Create community codes that link to formations  

Villars describes a number of community variants that are described in the chapters but not listed in the table of contents. So I took his table and did the following:  
1. Copied all natural community columns (1-6) into a single column and removed duplicates. This gave me a list of each community in his table.   
2. Copied the right three characters into a new column (cpage). He had the page number in his community description. This new column will be the primary key of the table.  
3. Stripped the page numbers from the community descriptions. I did this by taking the left of length defined by the length of the string minus the length of the page number (5).  
4. Add the form codes from the Table of Contents.

### Create schema and tables in postgres  

Created new schema in the vt_conservation database.  

```sql
CREATE SCHEMA nat_com
    AUTHORIZATION postgres;
```

Created tables.

```sql
CREATE TABLE nat_com.ctype (
   tpage INT PRIMARY KEY,
   type VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE nat_com.cform (
    fpage INT PRIMARY KEY,
    formation VARCHAR(40) UNIQUE NOT NULL,
	  tpage INT NOT NULL,
	FOREIGN KEY (tpage)
      REFERENCES nat_com.ctype (tpage)
);

CREATE TABLE nat_com.com (
    cpage SMALLINT PRIMARY KEY,
    community VARCHAR(60),
	  fpage SMALLINT NOT NULL,
	FOREIGN KEY (fpage)
      REFERENCES nat_com.cform (fpage)
);

CREATE TABLE nat_com.soil_com (
    ss_id VARCHAR(20) PRIMARY KEY,
    nc1 INT,
	  nc2 INT,
    nc3 INT,
    nc4 INT,
    nc5 INT,
    nc6 INT,
	FOREIGN KEY (nc1)
      REFERENCES nat_com.com (cpage),
  FOREIGN KEY (nc2)
      REFERENCES nat_com.com (cpage),
  FOREIGN KEY (nc3)
      REFERENCES nat_com.com (cpage),
  FOREIGN KEY (nc4)
      REFERENCES nat_com.com (cpage),
  FOREIGN KEY (nc5)
      REFERENCES nat_com.com (cpage),
  FOREIGN KEY (nc6)
      REFERENCES nat_com.com (cpage)   
);

CREATE TABLE nat_com.soil_series (
    mukey CHAR(6) PRIMARY KEY,
    ss_id VARCHAR(20),
    s_name VARCHAR(40),
    landform VARCHAR(60),
    FOREIGN KEY (ss_id)
        REFERENCES nat_com.soil_com (ss_id)
);

```

Add foreign key constraint ....

```SQL
ALTER TABLE nat_com.addison_soils
    ADD CONSTRAINT mukey_fkey FOREIGN KEY (mukey)
    REFERENCES nat_com.soil_series (mukey) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX fki_mukey_fkey
    ON nat_com.addison_soils(mukey);
```

Importing the data took a little effort. When I created the constraints through SQL prior to importing the data, if there was an error, the data simply wouldn't load and the error message was not specific enough to help troubleshoot. When I loaded the data into a table schema that lacked constraints and then tried to add constraints through the pgAdmin app, I found that the error messages were much more specific about the source of the error.  So unfortunately, I lost a lot of time yesterday to just getting the data into the database.

### Query for map layer  

The main trick here was that I needed LEFT JOINS for the natural community tables so that they would display even when blank. (Basically, I need the union rather than the intersection). If I used INNER JOINS, I would only retrieve records that had all of the natural community levels that I listed.

```sql
SELECT
	a.id,
	a.geom,
	b.s_name,
	e.formation,
	d.community AS nc1,
	f.community AS nc2,
	g.community AS nc3,
	h.community AS nc4
FROM nat_com.addison_soils AS a
INNER JOIN nat_com.soil_series AS b
ON a.mukey = b.mukey
INNER JOIN nat_com.soil_com AS c
ON b.ss_id = c.ss_id
LEFT JOIN nat_com.com AS d
ON c.nc1 = d.cpage
LEFT JOIN nat_com.cform AS e
ON d.fpage = e.fpage
LEFT JOIN nat_com.com as f
ON c.nc2 = f.cpage
LEFT JOIN nat_com.com as g
ON c.nc3 = g.cpage
LEFT JOIN nat_com.com as h
ON c.nc4 = h.cpage
;

ALTER TABLE nat_com.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);
```

### Distinguish Clayplain from Oak-Pine-NH Forest Formation  

I'd like this change to be simple and easily apply to the entire database. I think the easiest way to do it is to add "Clayplain Forest" as a separate Formation and then add "Forested wetland-upland matrix" as a new type. So I think this involves the following sequence:  

1. Update type table so that it includes the new type "Forested wetland-upland matrix".
2. Update form table so that it includes the new form "Clayplain Forest" with the new type foreign key.
3. Update com table so that the Valley Clayplain and Wet Valley Clayplain records have the Clayplain Forest foreign key.


```SQL
INSERT INTO nat_com.ctype(tpage, type)
VALUES (400, 'Forested Wetland-Upland Matrix');

INSERT INTO nat_com.cform(fpage, formation, tpage)
VALUES (400, 'Clayplain Forests', 400);

UPDATE nat_com.com
SET fpage = 400,
WHERE cpage = 174
OR cpage = 175;
```

So now I'll just repeat the TABLE query to kick out a layer for QGIS.

```sql
CREATE TABLE nat_com.nc_test AS
SELECT
	a.id,
	a.geom,
	b.s_name,
	e.formation,
	d.community AS nc1,
	f.community AS nc2,
	g.community AS nc3,
	h.community AS nc4
FROM nat_com.addison_soils AS a
INNER JOIN nat_com.soil_series AS b
ON a.mukey = b.mukey
INNER JOIN nat_com.soil_com AS c
ON b.ss_id = c.ss_id
LEFT JOIN nat_com.com AS d
ON c.nc1 = d.cpage
LEFT JOIN nat_com.cform AS e
ON d.fpage = e.fpage
LEFT JOIN nat_com.com as f
ON c.nc2 = f.cpage
LEFT JOIN nat_com.com as g
ON c.nc3 = g.cpage
LEFT JOIN nat_com.com as h
ON c.nc4 = h.cpage
;

ALTER TABLE nat_com.nc_test
    ADD CONSTRAINT nc_test_pkey PRIMARY KEY (id);

```

2.22 revision:

Split Clayplain into Valley Clayplain (84 - Upland Forest) and Wet Valley Clayplain as (244 - Wetland Forest)

```sql
CREATE TABLE nat_com.nc_test2 AS
SELECT
	a.id,
	a.geom,
	b.s_name,
	e.formation,
  i.type,
	d.community AS nc1,
	f.community AS nc2,
	g.community AS nc3,
	h.community AS nc4
FROM nat_com.addison_soils AS a
INNER JOIN nat_com.soil_series AS b
ON a.mukey = b.mukey
INNER JOIN nat_com.soil_com AS c
ON b.ss_id = c.ss_id
LEFT JOIN nat_com.com AS d
ON c.nc1 = d.cpage
LEFT JOIN nat_com.cform AS e
ON d.fpage = e.fpage
LEFT JOIN nat_com.ctype AS i
ON e.tpage = i.tpage
LEFT JOIN nat_com.com as f
ON c.nc2 = f.cpage
LEFT JOIN nat_com.com as g
ON c.nc3 = g.cpage
LEFT JOIN nat_com.com as h
ON c.nc4 = h.cpage
;

ALTER TABLE nat_com.nc_test2
    ADD CONSTRAINT nc_test2_pkey PRIMARY KEY (id);

```
