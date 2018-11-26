#The script will automate data downloading
import urllib

#Input Parameters here
fileDir = r'/home/david/data/GIS5578/maryland_imagery'
webaddress = r'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2013/treecover2000.txt'


#Use urllib to open the url and read it as text string
webpg = urllib.urlopen(webaddress)
data = webpg.read()

#Split the text string on the new line character
tiles = data.split('\n')


for c, tile in enumerate(tiles):
    imagename = "tile_%s" % (c)
    fileName = r"%s\%s" % (fileDir, imagename)
    print(tile,fileName)
    urllib.urlretrieve(tile, fileName)
    #Remove this after it works
    break
