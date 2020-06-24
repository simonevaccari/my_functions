# -*- coding: utf-8 -*-
"""
Created on March 2020 

@author: linuxuser

This file contains useful and common functions that I can call from any script, in order to simplify coding!

"""

# import libraries
from osgeo import gdal, gdal_array
import numpy as np
import scipy; from scipy import stats
import matplotlib
import matplotlib.pyplot as plt; from matplotlib import colors
import os

#cmap_code = 'RdYlBu' # the standard blue - red # here is the link of the color possibilities (http://matplotlib.org/examples/color/colormaps_reference.html, and here http://matplotlib.org/users/colormaps.html)
cmap_code = 'YlGn' # here is the link of the color possibilities (http://matplotlib.org/examples/color/colormaps_reference.html, and here http://matplotlib.org/users/colormaps.html)
nodata = -999 
nodata_0 = 0

def testF():
    my_str = 'Ciaoooooooooo'
    return my_str
    
######### PLOTTING ###############
def simple_2Dplot(ar1,ar2,maxX, maxY,xlab,ylab,title,show):
    plt.ioff()
    plt.figure()
    plt.plot(ar1,ar2,'.')
    plt.xlabel(xlab); plt.ylabel(ylab)
    plt.title(title)
    plt.xlim([0,maxX]); plt.ylim([0,maxY])
    #if show == True: 
    plt.show()
    plt.close()
    
  

def plot_ImgArray(array,norm_min,norm_max,title,show,save):
    """"HELP: this functions allows to plot a numpy array. Parameters are:
    array: the array to plot
    norm_min, norm_max: lim min and max where colors are stretched 
    title: title of the image plot
    show: boolean, do you want the image to display or not?"""
    plt.ioff() # so it doesnt display the figure if i save it! however if you set show=True it will show it anyway!! :)
    my_cmap = matplotlib.cm.get_cmap(cmap_code) # if you put an integer after cmap_code, it'll divide your colormap in that number of classes # here is the link of the color possibilities (http://matplotlib.org/examples/color/colormaps_reference.html, and here http://matplotlib.org/users/colormaps.html)
    my_cmap.set_under('w') # set the backgroudn (nodata) to white 'w'
    plt.figure()
    plt.imshow(array,norm=colors.Normalize(norm_min,norm_max),cmap=my_cmap)
    plt.colorbar()
    plt.title(title)
    if save[0] == True: plt.savefig(save[1],dpi=300)
    if show == True: plt.show()
    plt.close()


def plot_descreteVScontinouos():
    # NB!!! this function is just for notes, it is not a proper coded function!!

    # to plot continouos values
    plt.figure(); plt.imshow(MONTHLY_30m_CLASS2plot,cmap=my_cmap,norm=colors.Normalize(1,4)); 
    plt.colorbar(cmap=my_cmap, norm=colors.Normalize(1,4),ticks=[1,2,3,4,5])
                
    # to plot discrete colors  
    my_cmap = matplotlib.cm.get_cmap(cmap_code) # or if you want to define specific colors to use for your map: #cmap = colors.ListedColormap(['red', 'white', 'magenta', 'green'])
                                      
    bounds = [1,2,3,4,5] # bounds = labels; bounds.append(bounds[-1]+1)# this has to go one level up to the maximum entry! (ie up to 5, not 4) [1,2,3,4,5] # [0.5,1.5,2.5,3.5,4.5]
    norm = colors.BoundaryNorm(bounds, my_cmap.N)
    plt.figure(); plt.imshow(img,cmap=my_cmap,norm=norm); plt.colorbar(cmap=my_cmap, norm=norm, boundaries=bounds, ticks=bounds)

def plt_PieChart(sizes,labels,colors,title,show,save):
    plt.ioff()
    plt.figure()
    plt.pie(sizes,labels=labels,colors=colors, autopct='%1.1f%%', shadow=False)#, startangle=90)
    plt.title(title,bbox={'facecolor':'0.8', 'pad':10},loc='left')
    plt.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
    if save[0] == True: plt.savefig(save[1],dpi=300)
    if show == True: plt.show()

"""
def plotHist():
    #Histogram Examples to test
    data_hist = data.flatten() #[data!=np.nan]
    min_ = np.min(data_hist); max_ = np.max(data_hist); no_bins = (max_ - min_)/1000.
    plt.figure(); plt.hist(data_hist,bins=np.arange(min_,max_,no_bins)) ; plt.show() # check no_bins though and the np.arange function works properly
    plt.figure(); plt.hist(data_hist,bins=np.arange(min_,max_)) ; plt.show()
    """
        
# =============================
######### GDAL ARRAYS OPERATIONS ###########        
def getRasterInfo(rst):
    g = gdal.Open(rst)
    data = gdal_array.DatasetReadAsArray(g)
    xnum = g.RasterXSize; ynum = g.RasterYSize
    x_res = g.GetGeoTransform()[1]; y_res = g.GetGeoTransform()[5];
    minX = g.GetGeoTransform()[0]; maxY = g.GetGeoTransform()[3]; 
    maxX = minX + (x_res*xnum); minY = maxY + (y_res*ynum)
    extent = [minX, minY, maxX, maxY]
    return g,data, extent, round(x_res)

def clip_raster(rst2clp,clp_name,rst_clipped_name,px_res=str(30.)):
    print('Clip raster if not existing:')
    if not os.path.exists(rst_clipped_name): 
        print('Clipping raster with shapefile: ',)
        os.system('gdalwarp -dstnodata ' + str(nodata_0) + ' -q --config GDALWARP_IGNORE_BAD_CUTLINE YES -cutline ' + clp_name + ' -crop_to_cutline -tr ' + px_res + ' ' + px_res + ' -of GTiff ' + rst2clp + ' ' + rst_clipped_name)
        print('-> Successful') 
    else: print('File %s exists already. Delete/rename existing file is you want to update.' %rst_clipped_name)
    g,rst,ext,res = getRasterInfo(rst_clipped_name)
    return g,rst,ext,res


def shp2raster(sf_loc,sf_rst,extent,shp_field, pxl_res = 50, nodata = -999):
    print('rasterize..')
    gdal_str = 'gdal_rasterize -a ' + shp_field + ' -a_nodata ' + str(nodata) + ' -te ' + str(np.round(extent[0],2)) + ' ' + str(np.round(extent[1],2)) + ' ' + str(np.round(extent[2],2)) + ' ' + str(np.round(extent[3],2)) + ' -tr ' + str(pxl_res) + ' ' + str(-pxl_res) + ' -l ' + sf_loc[:-4].split('/')[-1] + ' ' + sf_loc + ' ' + sf_rst
    os.system(gdal_str)                    
    print('rasterize: DONE')

def createGeoTiff(filename, g, old_array_shape, new_array, data_type=gdal.GDT_Float32, noData = '', overwrite = 'yes'):
    """ Creates a new GeoTiff from an array.  Array parameters (i.e. pixel height/width,raster dimensions, projection info) are taken from a pre-existing geotiff.
    Geotiff output is GDT_Float32 by default

    Args:
    filename (str): absolute file path and name of the new Geotiff to be created
    g (gdal supported dataset object): This is returned from gdal.Open(filename) where filename is the name of a gdal supported dataset
    old_array_shape: shape(numpy array) result frm shape(). from which the new array's shape will be based on
    new_array: the array you want to write. 
    data_type (string): a string of teh data type for the output, e.g. gdal.GDT_Float32, gdal.GDT_Byte, GDT_Int16. Default is GDT_Float32

    Returns: None
    """
    
    # Error checking
    if isinstance(g, gdal.Dataset) == False:
        print('geoTiff.create2: g is not of type "gdal.Dataset". Skipping.')
        return
    
    #print(type(g))
    
    if os.path.exists(filename) and overwrite != 'yes':
        print("geoTiff.create2: file exists and overwrite is not 'yes'. Skipping.")
        print('geoTiff.create2:' + filename)
        return
    # main work:
    (X, deltaX, rotation, Y, rotation, deltaY) = g.GetGeoTransform()
    srs_wkt = g.GetProjection()
    driver = gdal.GetDriverByName("GTiff")

    Nx = old_array_shape[-2]
    Ny = old_array_shape[-1]
    
    s0average = driver.Create(filename, Ny, Nx, 1, data_type) 
    s0average.SetGeoTransform((X, deltaX, rotation, Y, rotation, deltaY))
    s0average.SetProjection(srs_wkt)

    if noData == '':
        noData = s0average.GetRasterBand(1).GetNoDataValue()
        #print('noData = ' + str(noData))
    else:
        s0average.GetRasterBand(1).SetNoDataValue(noData)
        #print('noData = ' + str(noData))
    #print('geoTiff.create2: writing: '+ filename)
    s0average.GetRasterBand(1).WriteArray(new_array)
    s0average = None
       
    
############ MATHS AND STATISTICS ##########   
def print_Min_and_Max(arr,name):
    print('Min and Max. - ', name, ' - Shape:',np.shape(arr))
    print('Min:\t', np.min(arr), '\tMax:\t', np.max(arr), '\nNanMin:\t', np.nanmin(arr), '\tNanMax:\t', np.nanmax(arr),'\n')

def normalize_data(data,data_min,data_max,norm_min,norm_max): 
    # video How To Normalize Data here: http://www.howcast.com/videos/359111-how-to-normalize-data/
    A = data_min; B = data_max
    a = norm_min; b = norm_max
    data_norm = a + (data-A)*(b-a)/(B-A)
    return data_norm
    
def linear_regression(ar1,ar2):
    #print('means:', np.mean(ar1), np.mean(ar2))
    linefit = stats.linregress(ar1,ar2) # returns a 5 element array, containing 0-slope, 1-intercept, 2-rvalue, 3-pvalue, 4-stderr
    m = linefit[0]; q = linefit[1]; r2 = linefit[2]**2; pv=linefit[3]; se=linefit[4]
    return m,q,r2,pv,se  

def poly_regression(ar1,ar2,maxX,maxY,xlab,ylab,title,degree,show,save):
##~~~~~~~~~~~~~~~~~~~~~~~~~~
#    #original polinomial script    
#    coefficients = np.polyfit(ar1,ar2,degree) # returns the polynomial coefficients, highest power first 
#    mypoly = np.poly1d(coefficients)
#    plt.plot(ar1,mypoly(ar1),'--b')
#    if show == True: plt.show()
##~~~~~~~~~~~~~~~~~~~~~~~~~~
    plt.figure()
    plt.plot(ar1,ar2,'.k',markersize=1)     
    
    # create polynomial equation coefficients
    coefficients = np.polyfit(ar1,ar2,degree) # returns the polynomial coefficients, highest power first 
    mypoly = np.poly1d(coefficients)
    print(coefficients)
    
    # create regression equation (regline) label
    eq_text = 'y = ' + str(np.round(coefficients[0],2)) + ' * x^2 ' + str(np.round(coefficients[1],2)) + ' * x ' + str(np.round(coefficients[2],2))

    # create regline and 1:1 line
    a1 = np.arange(0,maxX,maxX/100.); plt.plot(a1,a1,'--c') # 1:1 line
    a2 = np.arange(0,max(ar1),max(ar1)/100.); plt.plot(a2,mypoly(a2),'--r') 
    #plt.plot(ar1,ar2,'.k',a2,mypoly(a2),'--r')# plot data AND poly regression line  
    plt.annotate('1:1 line',xy=(0.02,0.9),color='c') # 1:1 line annotation
    plt.annotate(eq_text,xy=(0.02,0.8),color='r') # regression equation and r2

#    if len(save)==2:
#        # write out a txt file with equation and r2
#        filetxt = open(save[1][:-4]+'.txt','wb')
#        filetxt.write(eq_text)
#        filetxt.close()

    # general plot parameters
    plt.xlim([0,maxX]); plt.ylim([0,maxY])
    plt.xlabel(xlab); plt.ylabel(ylab)
    plt.title(title)
    if save[0] == True: plt.savefig(save[1],dpi=300)
    if show == True: plt.show()
    plt.close()    
