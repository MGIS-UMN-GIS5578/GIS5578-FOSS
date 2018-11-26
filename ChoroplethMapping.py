import geopandas
import matplotlib.pyplot as plt


#Import shapefile and read it geopandas, create a dataframe object
shapefile = r"/home/david/data/bo_1976_2001_hflad_geo1a_bo.shp"
df = geopandas.read_file(shapefile)

#Use the dataframe object to plot the file
df.plot()
plt.show()

#Use index slicing to choose the first feature in the shapefile.
#This will plot on it own
df.ix[0].geometry

#Get the shapefile column/field names
df.columns

#Select a column of data in the shapefile using the field name
df.label

#Choropleth mapping
df.plot(column='label', cmap='OrRd');
plt.show()




