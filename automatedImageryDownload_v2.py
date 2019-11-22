# The script will automate data downloading of satellite imagery
# This data comes from the University of Maryland
# http://data.globalforestwatch.org/

import urllib
import os

#Input Parameters here
fileDir = r'c:\work\imagery'
webaddress = r'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2013/treecover2000.txt'


#Use urllib to open the url and read it as text string
webpg = urllib.request.urlopen(webaddress)
data = webpg.read()

#Split the text string on the new line character
tiles = data.decode("utf-8").split('\n')

#loop for downloading the data
for c, tile in enumerate(tiles):
    imagename = "tile_%s" % (c)
    fileName = os.path.join(fileDir, ".".join([imagename, "tif"]))
    print(tile,fileName)
    urllib.request.urlretrieve(tile, fileName)
    #Remove this after it works
    if c == 10: break
