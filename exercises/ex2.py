
# coding: utf-8

# # Exercise 2
#
#
# Add a value from a raster to a points shape.
#
# Input files:
# * output/vector/bandijk.shp  (see Exercise 1)
# * input/vector/model_extent.shp
# * input/raster/ahn3/m_40cz2.tif
#

# In[ ]:


import os
import sys
import subprocess

# define GRASS Database
# add your path to grassdata (GRASS GIS database) directory
# gisdb = os.path.join(os.path.expanduser("~"), "grassdata")
# the following path is the default path on MS Windows
gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")
gisdb = gisdb.replace("C:\\Users\\","D:\\")

# specify (existing) Location and Mapset
location = "RD_new"
mapset = "mapset1"

# path to the GRASS GIS launch script
# we assume that the GRASS GIS start script is available and on PATH
# query GRASS itself for its GISBASE
# (with fixes for specific platforms)
# needs to be edited by the user
grass7bin = 'grass72'
if sys.platform.startswith('win'):
    # MS Windows
    grass7bin = r'grass72.bat'
    # uncomment when using standalone WinGRASS installer
    # grass7bin = r'C:\Program Files (x86)\GRASS GIS 7.2.0\grass72.bat'
    # this can be avoided if GRASS executable is added to PATH
elif sys.platform == 'darwin':
    # Mac OS X
    # TODO: this have to be checked, maybe unix way is good enough
    grass7bin = '/Applications/GRASS/GRASS-7.2.app/'

# query GRASS GIS itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
try:
    p = subprocess.Popen(startcmd, shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except OSError as error:
    sys.exit("ERROR: Cannot find GRASS GIS start script"
             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
if p.returncode != 0:
    sys.exit("ERROR: Issues running GRASS GIS start script"
             " {cmd}: {error}"
             .format(cmd=' '.join(startcmd), error=err))
gisbase = out.strip(os.linesep)

# set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# define GRASS-Python environment
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)

# import (some) GRASS Python bindings
import grass.script as gscript
import grass.script.setup as gsetup

# launch session
rcfile = gsetup.init(gisbase, gisdb, location, mapset)

# example calls
gscript.message('Current GRASS GIS 7 environment:')
print gscript.gisenv()


# In[ ]:


# 1. Load model extent
# (hint) https://grass.osgeo.org/grass72/manuals/v.in.ogr.html
gscript.run_command('g.remove', type = "vector", name = 'extent', flags="f", quiet=True)
gscript.run_command('v.in.ogr', input = 'input/vector/model_extent.shp', output = "extent", quiet=True)


# In[ ]:


# 2. Set GRASS region
# (hint) https://grass.osgeo.org/grass72/manuals/g.region.html
gscript.run_command('g.region', vector = "extent", res=1)


# In[ ]:


# 3. Load raster
gscript.run_command('g.remove', type = "raster", name = 'ahn3', flags="f", quiet=True)
gscript.run_command('r.in.gdal', input = 'input/raster/ahn3/m_40cz2.tif', output = "ahn3", quiet=True)


# In[ ]:


# 4. Load points shape
gscript.run_command('g.remove', type = "vector", name = 'bandijk_10', flags="f", quiet=True)
gscript.run_command('v.in.ogr', input = 'output/bandijk_10.shp', output = "bandijk_10", quiet=True)


# In[ ]:


# 5. Make a copy of the vector data
gscript.run_command('g.copy', vect='bandijk_10,bandijk_10_height')


# In[ ]:


# 6. Add column to the points to store the height
# see https://grass.osgeo.org/grass72/manuals/v.db.addcolumn.html
gscript.run_command('v.db.addcolumn', map='bandijk_10_height', columns="height double precision")


# In[ ]:


# 7. Query raster by points and store the height
# see https://grass.osgeo.org/grass72/manuals/v.what.rast.html
gscript.run_command('v.what.rast',map='bandijk_10_height',raster='ahn3', column='height')


# In[ ]:


# 8. Add geometry to database
gscript.run_command('v.info', map='bandijk_10_height', flags="c")
gscript.run_command('v.db.addcolumn', map='bandijk_10_height', columns="x double precision, y double precision")
gscript.run_command('v.to.db', map='bandijk_10_height', option='coor', col='x,y')


# In[ ]:


# 9. Write to xyz
outputdir = 'output'
gscript.run_command('v.db.select',map='bandijk_10_height', column='x,y,height', 
                    file=os.path.join(outputdir,'bandijk_10_height.xyz'), separator='space', flags="c", overwrite=True)


# In[ ]:


# Remove data (if required)
# gscript.run_command('g.remove', type = "vector", name = 'extent', flags="f", quiet=True)

#for vect in gscript.list_strings(type='vector'):
#    gscript.run_command('g.remove', type = "vector", name = vect, flags="f", quiet=True)
#
#for rast in gscript.list_strings(type='raster'):
#    gscript.run_command('g.remove', type = "raster", name = vect, flags="f", quiet=True)


# In[ ]:


# Delete the session file
os.remove(rcfile)
