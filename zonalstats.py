from osgeo import gdal, ogr
from collections import Counter
import numpy as np
import timeit, os


def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / xDist)
    
    return (pixel, line)
    

def Pixel2world(geoMatrix, row, col):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the x,y location of a pixel location
    """

    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    x_coord = (ulX + (row * xDist))
    y_coord = (ulY - (col * xDist))

    return (x_coord, y_coord)


def RasterizePolygon(inRasterPath, outRasterPath, vectorPath):
    ''' Convert the vector dataset into a raster with the same spatial extent as raster'''
    #The array size, sets the raster size 
    inRaster = gdal.Open(inRasterPath)
    rasterTransform = inRaster.GetGeoTransform()
    pixel_size = rasterTransform[1]
    
    #Open the vector dataset
    vector_dataset = ogr.Open(vectorPath)
    theLayer = vector_dataset.GetLayer()
    geomMin_X, geomMax_X, geomMin_Y, geomMax_Y = theLayer.GetExtent()
    
    outTransform= [geomMin_X, rasterTransform[1], 0, geomMax_Y, 0, rasterTransform[5] ]
    
    rasterWidth = int((geomMax_X - geomMin_X) / pixel_size)
    rasterHeight = int((geomMax_Y - geomMin_Y) / pixel_size)
    
    #MRaster Driver
    tiffDriver = gdal.GetDriverByName('GTiff')
    
    #Global Raster
    theRast = tiffDriver.Create(outRasterPath, inRaster.RasterXSize, inRaster.RasterYSize, 1, gdal.GDT_Int16, ['COMPRESS=LZW'])
    
    #os.chmod(outRasterPath, 0777)
    theRast.SetProjection(inRaster.GetProjection())
    theRast.SetGeoTransform(rasterTransform)
    
    band = theRast.GetRasterBand(1)
    band.SetNoDataValue(-999)

    #Rasterize
    gdal.RasterizeLayer(theRast, [1], theLayer, options=["ATTRIBUTE=id"])
    
    del theRast, inRaster

    
def ClipRaster(inRasterPath,clippedPath, vectorPath):
    '''This function clips the raster to the extent of the polygon '''
    
    vector_dataset = ogr.Open(vectorPath)
    theLayer = vector_dataset.GetLayer()
    geomMin_X, geomMax_X, geomMin_Y, geomMax_Y = theLayer.GetExtent()
    #print(geomMin_X, geomMax_X, geomMin_Y, geomMax_Y) 

    inRaster = gdal.Open(inRasterPath)
    band = inRaster.GetRasterBand(1)
    
    rasterTransform = inRaster.GetGeoTransform()
    pixel_size = rasterTransform[1]
    
    ulY, ulX = world2Pixel(inRaster.GetGeoTransform(), geomMin_X, geomMax_Y )
    lrY, lrX = world2Pixel(inRaster.GetGeoTransform(), geomMax_X, geomMin_Y )
    #print(ulY, ulX, lrY, lrX)
    
    imageHeight = abs(int(lrX - ulX))
    imageWidth = abs(int(ulY - lrY))

    coordBottomRight = Pixel2world(inRaster.GetGeoTransform(), ulY, ulX)
    coordTopLeft = Pixel2world(inRaster.GetGeoTransform(), lrY, lrX)

    #print(coordBottomRight, coordTopLeft)

    outTransform= [coordBottomRight[0], pixel_size, 0, coordBottomRight[1], 0, rasterTransform[5] ]
    
    #rasterWidth = int((geomMax_X - geomMin_X) / pixel_size)
    #rasterHeight = int((geomMax_Y - geomMin_Y) / pixel_size)
    
    tiffDriver = gdal.GetDriverByName('GTiff')
    clippedRaster = tiffDriver.Create(clippedPath, imageWidth, imageHeight, 1, gdal.GDT_Int16, ['COMPRESS=LZW'])
    #band.DataType
    
    outputArray = inRaster.ReadAsArray(xoff=ulY, yoff=ulX, xsize=imageWidth, ysize=imageHeight)
    
    clippedRaster.SetProjection(inRaster.GetProjection())
    clippedRaster.SetGeoTransform(outTransform)
    
    theBandRast = clippedRaster.GetRasterBand(1)    
    theBandRast.SetNoDataValue(-999)
    theBandRast.WriteArray(outputArray)
    
    del inRaster, clippedRaster


def CalculateZonalStats(clippedRasterPath, maskedRasterPath):
    '''Function for conducting zonal statistics '''

    dataRaster = gdal.Open(clippedRasterPath)
    dataArray = dataRaster.ReadAsArray()

    maskedRaster = gdal.Open(maskedRasterPath)
    maskedArray = maskedRaster.ReadAsArray()

    polygonIDS, polygonCounts = np.unique(maskedArray, return_counts=True)

    ZonalStats = {}
    for id in polygonIDS[1:]:
        maskedRaster = np.ma.masked_where(maskedArray != id, dataArray)
        ZonalStats[str(id)] = {'min': maskedRaster.min(), 'max': maskedRaster.max(), 'avg': maskedRaster.mean()}

    return ZonalStats
    #np.nditer((dataArray,maskedArray), op_flags=['readonly'] )



####################### Code Starts #############################

workingDir = r"c:\git\GIS5578-FOSS\datasets"
rasterPath = os.path.join(workingDir, "glc2000.tif")
vectorPath = os.path.join(workingDir, "states.shp")

outDir = r"c:\work"
rasterClipPath= os.path.join(outDir,"glc2000_us.tif")
rasterizedVectorPath = os.path.join(outDir,"us_states_glc2000.tif")

start = timeit.default_timer()
print("Starting....")
ClipRaster(rasterPath,rasterClipPath, vectorPath)
RasterizePolygon(rasterClipPath, rasterizedVectorPath, vectorPath)
print("Clipped and Rasterized Raster")

print("Calculating Zonal Statistics")
zonalStats = CalculateZonalStats(rasterClipPath, rasterizedVectorPath)
print(zonalStats)
stop = timeit.default_timer()
print("Took %s seconds" % (stop-start) )
# npit = np.nditer( [maskedArray,rasterArray], [], [['readonly'], ['readonly']])


