# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:11:58 2019
Script for automating LISA Analyses

I used geopandas to read an existing shapefile and perform a spatial measure
PySAL will be used to perform the spatial measure (LISA)
@author: dahaynes
"""



import pysal, geopandas

shpFilePath = r"C:\git\GIS5578-FOSS\datasets\mn_tracts_2010.shp"
tractsDF = geopandas.read_file(shpFilePath)


        #Generate once per loop
weights = pysal.weights.Queen.from_dataframe(tractsDF)
tractsDF.keys()

nationalDeprivationScores = tractsDF['national_a']
percentMinority = tractsDF['percent_mi']
                
bivariateLisa = pysal.pysal.Moran_Local_BV(nationalDeprivationScores, percentMinority, weights, permutations=999)
for recordName, recordValues in zip(['lisa','p_value', 'quadrant'], [bivariateLisa.Is, bivariateLisa.p_sim, bivariateLisa.q] ):
    tractsDF.insert(len(tractsDF.keys()), recordName, recordValues)
            

del tractsDF['geometry']

tractsDF.to_csv(r"E:\work\bivariate_list.csv", sep=',')
print("Finished")