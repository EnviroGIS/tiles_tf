from PyQt4.QtCore import QVariant
from PyQt4.QtGui import *
from qgis.core import QgsApplication
from qgis.core import QgsRasterLayer
import processing
from qgis.gui import *
import os

from PyQt4.QtGui import QInputDialog

# add grid layer. Will be used for clipping the raster
def addGrid(input):
    cellsize = QInputDialog.getText(None, 'Cell Size', 'Enter the cell size (meters): ')
    cellsize = int(cellsize[0]) # first calue from tuble (cellsize, True)
    crs = "EPSG:3857" #Pseudo Mercator System 
    xmin = (input.extent().xMinimum()) #extract the minimum x coord from our layer
    xmax =  (input.extent().xMaximum()) #extract our maximum x coord from our layer
    ymin = (input.extent().yMinimum()) #extract our minimum y coord from our layer
    ymax = (input.extent().yMaximum()) #extract our maximum y coord from our layer
    #prepare the extent in a format the VectorGrid tool can interpret (xmin,xmax,ymin,ymax)
    extent = str(xmin)+ ',' + str(xmax)+ ',' +str(ymin)+ ',' +str(ymax)  
    grid = "E:/desktop/raster/grid.shp"
    processing.runalg('qgis:vectorgrid',  extent, cellsize, cellsize,  0, grid)
    print 'Done. Grid is created'
    return grid

# add column for TensorFlow classification
def addColumn(layer):
    layer.dataProvider().addAttributes([QgsField("tilename", QVariant.String)])
    layer.dataProvider().addAttributes([QgsField("tileclass", QVariant.String)])
    layer.updateFields()
    print 'Columns are added'

# create folders for classificated tiles
def addFolder(layer):
    os.makedirs("E:/desktop/raster/tiles/tr")
    os.makedirs("E:/desktop/raster/tiles/val")
    l = []
    for f in layer.getFeatures():
        idx = layer.fieldNameIndex( "tileclass" )
        if f[idx] == NULL:
            continue
        else:
            if f[idx] not in l: 
                l.append(f[idx])
                os.makedirs("E:/desktop/raster/tiles/tr/"+ str(f[idx]))
                os.makedirs("E:/desktop/raster/tiles/val/"+ str(f[idx]))
            else:
                continue
    os.makedirs("E:/desktop/raster/tiles/raw")

# clip raster to tiles
def clipData(layer, raster_layer):
    dataset_file = open('E:/desktop/raster/tr_dataset.txt', 'w')
    val_dataset_file = open('E:/desktop/raster/val_dataset.txt', 'w')
    code = 1
#    selection = []
    for f in layer.getFeatures():
#        print 'Selecting feature'
#        selection.append(f.id())
#        layer.setSelectedFeatures(selection)
#        print 'Feature has been selected'
#        iface.mapCanvas().refresh()
        bbox = f.geometry().boundingBox()
        bbox_extent = '%f,%f,%f,%f' % (bbox.xMinimum(), bbox.xMaximum(), bbox.yMinimum(), bbox.yMaximum())
        if code % 100 == 0:
            print code, 'tiles created'
        idx = layer.fieldNameIndex( "tileclass" )
        if f[idx] == NULL:
            processing.runalg('gdalogr:cliprasterbyextent',raster_layer,"0", bbox_extent,5,4,75,6,1,False,0,False,"","E:/desktop/raster/tiles/raw/" + str(10000 + code)+".png")
        else:
            if code % 3 == 0: #txt for validation dataset
                processing.runalg('gdalogr:cliprasterbyextent',raster_layer,"0", bbox_extent,5,4,75,6,1,False,0,False,"","E:/desktop/raster/tiles/val/"+ str(f[idx])+"/" + str(10000 + code)+".png")
                val_dataset_file.write("tiles/val/" + str(f[idx]) +"/"+ str(10000 + code)+".png " + str(f[idx]) +"\n")
            else: # txt for learning dataset
                processing.runalg('gdalogr:cliprasterbyextent',raster_layer,"0", bbox_extent,5,4,75,6,1,False,0,False,"","E:/desktop/raster/tiles/tr/"+ str(f[idx])+"/" + str(10000 + code)+".png")
                dataset_file.write("tiles/tr/" + str(f[idx]) +"/"+ str(10000 + code)+".png " + str(f[idx]) +"\n")
        with edit(layer):
            idx = layer.fieldNameIndex( "tilename" )
            f[idx] = str(10000 + code)
            layer.updateFeature(f)
        code = code + 1

raster_layer = QgsRasterLayer("E:/desktop/raster/test.tif", "test_area")

while True:
    q = QInputDialog.getText(None, 'Grid Layer', 'Do you have specific grid layer? (y/n): \nIf not it would be created')
    if q[0] == 'n':
        # creates vector grid
        grid_layer_url = addGrid(raster_layer)
        
        # loads vector grid to QGIS Project
        grid_layer = iface.addVectorLayer(grid_layer_url, "gridlayer", "ogr")
        
        # add columns required for tiles creation
        addColumn(grid_layer)
        
        break
    elif q[0] == 'y':
        path = QInputDialog.getText(None, 'Grid Layer', 'Enter the path to your Grid Shapefile: ')
        grid_layer = QgsVectorLayer(path[0], "gridlayer", "ogr")
        break
    elif q[0] == 'quit':
        break
    else:
        print "For exiting please type 'quit' (with no quates)"
        continue

print 'Now you could classify tiles by yourself\nYou could skip this step if you want to create tileset with no classification data'

while True:
    q = QInputDialog.getText(None, 'Grid Layer', 'Ready to continue? (y/n): ')
    if q[0] == 'y':
        addFolder(grid_layer)
        print 'Folders added\nPreparing to clip images'
        clipData(grid_layer, raster_layer)
        break
    elif q[0] == 'quit':
        break
    else:
        print "For exiting please type 'quit' (with no quates)"
        continue 