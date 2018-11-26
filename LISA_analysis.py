# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:09:13 2018
Script for automating LISA Analyses
I used geopandas as you can create a geospatial dataframe (in memory shapefile) 
Which can be connecte to PySAL. Very clean and neat

@author: dahaynes
"""

import pysal, psycopg2, geopandas
from psycopg2 import extras
            


def ConnectDatabase(host, db, port, user):
    """
    This function creates the postgresql connection
    """
    connection = psycopg2.connect(host=host, database=db, port=port, user=user)
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
    
    return connection, cursor


conn, cur = ConnectDatabase('localhost', 'research', 5432, 'david')

msa = ['Los Angeles-Long Beach-Anaheim, CA', 'Baltimore-Columbia-Towson, MD', 'Boston-Cambridge-Newton, MA-NH', 'New York-Newark-Jersey City, NY-NJ-PA','Chicago-Naperville-Elgin, IL-IN-WI']
attributes = ['onsale_97', 'offsale_97', 'onsale_area_97', 'offsale_area_97']

regionFrames = []
for m in msa:
    lisaDataFrames = []
    for counter, a in enumerate(attributes):
        
        query = """with msa_region as
        (
        SELECT p.statefp00::bigint as state_fips, p.gisjoin, p.ctidfp00::bigint as geoid, p.geom, m.name
        FROM continental_us_tract_2000 p 
        inner join MSA_2016 m on ST_Intersects(m.geom, p.geom) and ST_Within(ST_Centroid(p.geom), m.geom)
        WHERE m.name = '%s'
        )
        SELECT p.geoid, p.gisjoin, CASE when %s is NULL THEN 0 ELSE %s END as record, p.geom as geometry
        FROM msa_region p left join info_usa_alcohol_outlets a on (p.geoid = a.geo2000)""".replace("\n","") % (m, a, a, )
    
    
        print(counter, query)
        dataFrame = geopandas.GeoDataFrame.from_postgis(query, conn, geom_col='geometry')
        #Generate once per loop
        if counter == 0: weights = pysal.weights.Queen.from_dataframe(dataFrame)
        values = dataFrame['record']
        lisa = pysal.Moran_Local(values, weights, permutations=999)
        
        #Attribute names get specified
        lisaDF = geopandas.pd.DataFrame( {a:values, 'lisa_%s' % (a,): lisa.Is, 'p_value_%s' % (a,): lisa.p_sim} )        
        
        lisaDataFrames.append(lisaDF)
    
    lisaDataFrames.insert(0, dataFrame)
    regionDataFrame = geopandas.pd.concat(lisaDataFrames, axis=1)    
    regionFrames.append(regionDataFrame)
    

conn.close()
dataset = geopandas.pd.concat(regionFrames, keys=msa, axis=0)
del dataset['geometry']
del dataset['record']
dataset.to_csv(r"C:\osypuk\lisa\region_analytics3.csv", sep=',')
print("Finished")
    

    

