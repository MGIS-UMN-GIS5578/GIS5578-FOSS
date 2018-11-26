#The script will automate data downloading
#David Haynes

import urllib

#Input Parameters here
fileDir = r"e:\maryland_imagery"
webaddress = r'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2013/treecover2000.txt'


#Use urllib to open the url and read it as text string
webpg = urllib.request.urlopen(webaddress)
data = webpg.read()

#Split the text string on the new line character
tiles = data.split(b'\n')


for c, tile in enumerate(tiles):
    imagename = "tile_%s" % (c)
    fileName = r"%s\%s.tif" % (fileDir, imagename)
    print(tile,fileName)
    urllib.request.urlretrieve(tile.decode("utf-8"), fileName)
    #Remove this after it works
    break
