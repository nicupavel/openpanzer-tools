# Using

``` icons_convert.py <unit images list file> <folder containing extracted unit icons>```

# Unit images list file
This file is generated when _equipment/equipment_convert.py_ script is run and placed in the corresponding 
equipment folder as **icons.list** 

# Extracting unit icons
If you add a new equipment for the first time in the game you will have to extract and add icons.
1. Use SHPTool.exe and load Panzer2.dat file (this file should correspond with the equipment being used)
2. Go to  Tools > Dat Tool > Unpack (there is an Unpack button on the toolbar (3 floppy-disk icon)) all icons to disk in a folder you specify.
3. Go to Tools > Shp Tool > Select SHP Folder where you unpacked in step 1
4. Save as BMP > Convert SHP files in a folder to BMP > Select 1x9 format > OK
5. The BMP files should now be extracted to same folder (the UI looks like it's frozen but it works)

# rename_list.txt

If you wish to replace the equipment image used by certain unit with a custom one add the transition here. 

# OpenIcons alternative

Instead of extracting icons yourself it's also possible to use OpenIcons project. Beware that 
some icons might not exist in OpenIcons.

To obtain OpenIcons use:
```
svn checkout https://svn.code.sf.net/p/opengeneral/code/ svn-opengeneral
```
OpenIcons is a community effort to create and enhance unit icons for Luis Guzman [Open General](http://www.luis-guzman.com/).


# Important
The zdXXX.png icons are actually adXXX.png icons. We renamed these icons in equipment convert script to get rid
of adblocker issues on most browsers.

```ad03.png zd03.png
ad04.png zd04.png
ad08.png zd08.png
ad09.png zd09.png
ad10.png zd10.png
ad11.png zd11.png
ad12.png zd12.png
ad13.png zd13.png
ad14.png zd14.png
ad19.png zd19.png
ad20.png zd20.png
ad21.png zd21.png
ad22.png zd22.png
ad23.png zd23.png
ad24.png zd24.png
ad25.png zd25.png
ad26.png zd26.png
adeth.png zdeth.png
adpt1.png zdpt1.png
adzer.png zdzer.png
```