REM
REM Environmental variables for GRASS OSGeo4W installer
REM

SET OSGEO4W_ROOT=C:\PROGRA~1\QGIS2~1.18

set path=%PATH%;%OSGEO4W_ROOT%\bin;%WINDIR%\system32;%WINDIR%;%WINDIR%\system32\WBem

rem
rem Set environmental variables
rem
REM call %OSGEO4W_ROOT%\bin\o4w_env.bat  (except python-core.bat)
call %OSGEO4W_ROOT%\etc\ini\gdal.bat
call %OSGEO4W_ROOT%\etc\ini\libgeotiff.bat
call %OSGEO4W_ROOT%\etc\ini\libjpeg.bat
call %OSGEO4W_ROOT%\etc\ini\liblas.bat
call %OSGEO4W_ROOT%\etc\ini\msvcrt.bat
call %OSGEO4W_ROOT%\etc\ini\proj.bat
call %OSGEO4W_ROOT%\etc\ini\qt4.bat
call %OSGEO4W_ROOT%\etc\ini\rbatchfiles.bat

set GISBASE=%OSGEO4W_ROOT%\apps\grass\grass-7.2.1

REM Uncomment if you want to use Bash instead of Cmd
REM Note that msys package must be also installed
REM set GRASS_SH=%OSGEO4W_ROOT%\apps\msys\bin\sh.exe

REM set GRASS_PYTHON=%OSGEO4W_ROOT%\bin\python.exe
REM set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27

set GRASS_PROJSHARE=%OSGEO4W_ROOT%\share\proj

set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set GEOTIFF_CSV=%OSGEO4W_ROOT%\share\epsg_csv

set FONTCONFIG_FILE=%GISBASE%\etc\fonts.conf

REM set RStudio temporarily to %PATH% if it exists

IF EXIST "%ProgramFiles%\RStudio\bin\rstudio.exe" set PATH=%PATH%;%ProgramFiles%\RStudio\bin

REM set R_USER if %USERPROFILE%\Documents\R\ exists to catch most common cases of private R libraries
IF EXIST "%USERPROFILE%\Documents\R\" set R_USER=%USERPROFILE%\Documents\
