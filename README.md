# This ReadMe is for understanding how to build your own conda environment

The beauty of doing this is that Anaconda you will provide stable package installation.
This should work 90% of the time

1. [Create a conda environment](https://towardsdatascience.com/getting-started-with-python-environments-using-conda-32e9f2779307) 
```
conda create --name geoanalyst python=3.6, jupyter notebook
```
1. Activates your conda environment
```
source activate geoanalyst
```

1. Install your packages
I strongly recommend verified packages from [Conda-Forge](https://conda-forge.org/)
### GDAL
Use GDAL Version 2.2 or greater gdal=2.2.0
```
conda install -c conda-forge gdal
```
## Down Stream Packages that build upon others (Dependencies)
```
conda install -c conda-forge geopandas
```
[Geopandas](http://geopandas.org/install.html)

Dependencies
Required dependencies:
1. numpy
1. pandas (version 0.23.4 or later)
1. shapely (interface to GEOS)
1. fiona (interface to GDAL)
1. pyproj (interface to PROJ)
1. six
Optional dependencies are:
1. rtree (optional; spatial index to improve performance and required for overlay operations; interface to libspatialindex)
1. psycopg2 (optional; for PostGIS connection)
1. geopy (optional; for geocoding)
1. matplotlib (>= 2.0.1)
1. descartes

## I recommend these libraries
conda install -c conda-forge psycopg2  #For working with databases
conda install -c conda-forge georasters
conda install -c conda-forge geojson
conda install -c anaconda beautifulsoup4 

## GeoVisualization
1. Folium
```
conda install folium -c conda-forge
```
2. Bokeh
```
conda install bokeh
```