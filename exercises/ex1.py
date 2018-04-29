
# coding: utf-8

# # Exercise 1
# 
# 
# Create a points shape with points every 10 m along a line.
# 
# Input files: 
# * input/vector/bandijk.shp
# * input/vector/model_extent.shp

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
gscript.run_command('g.region', vector = "extent", res=5)


# In[ ]:


# 3. Load line vector into GRASS map
gscript.run_command('g.remove', type = "vector", name = 'bandijk', flags="f", quiet=True)
gscript.run_command('v.in.ogr', input = 'input/vector/bandijk.shp', output = "bandijk", quiet=True)


# In[ ]:


# 4. Create a points shape with points every 10 m
# (hint) https://grass.osgeo.org/grass72/manuals/v.to.points.html

gscript.run_command('g.remove', type = "vector", name = 'bandijk_10', flags="f", quiet=True)
gscript.run_command('v.to.points', input = 'bandijk', dmax=10, output = "bandijk_10", flags="i", quiet=True)


# In[ ]:


# 5. Save to shapefile
# (hint) https://grass.osgeo.org/grass72/manuals/v.out.ogr.html
outputdir = 'output'
if not os.path.exists(outputdir):
    os.mkdir(outputdir)
gscript.run_command('v.out.ogr', 
                    input = "bandijk_10", 
                    output = os.path.join(outputdir,'bandijk_10.shp'), 
                    overwrite=True, quiet=True)


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

