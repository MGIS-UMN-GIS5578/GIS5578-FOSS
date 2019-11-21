# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:11:58 2019
Script for automating LISA Analyses

I used geopandas to read an existing shapefile and perform a spatial measure
PySAL will be used to perform the spatial measure (LISA)
@author: dahaynes
"""



import pysal, geopandas, pandas

shpFilePath = r"C:\git\GIS5578-FOSS\datasets\us_counties.shp"
deprivationData = r"C:\git\GIS5578-FOSS\datasets\deprivation_index_2013_tract.csv"

countiesDF = geopandas.read_file(shpFilePath)
# countiesDF.STATEFP10.unique() returns unique values
# This selects just the minnesota data
mnCounties = countiesDF.loc[countiesDF['STATEFP10'] == '27']
# Saving this to a new shapefile
mnCounties.to_file(r"c:\work\mn_counties.shp", driver='ESRI Shapefile')
deprivationDF = pandas.read_csv(deprivationData)

mnCounties.join(other.set_index('key'), on='GISJOIN')


        #Generate once per loop
weights = pysal.weights.Queen.from_dataframe(mnCounties)
nationalDeprivationScores = dataFrame['national_average']
percentMinority = dataFrame['percent_minority']
                
bivariateLisa = pysal.pysal.Moran_Local_BV(nationalDeprivationScores, percentMinority, weights, permutations=999)
for recordName, recordValues in zip(['lisa','p_value', 'quadrant'], [bivariateLisa.Is, bivariateLisa.p_sim, bivariateLisa.q] ):
    dataFrame.insert(len(dataFrame.keys()), recordName, recordValues)
            

del dataFrame['geometry']

dataFrame.to_csv(r"E:\git\analyzing_nursing_facilities\datasets\bivariate_list.csv", sep=',')
print("Finished")