#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      cschultz
#
# Created:     06/12/2018
# Copyright:   (c) cschultz 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

start = time.time()

arcpy.env.overwriteOutput = True

inFile = open("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\InfoUpdateTable_log.txt", "w")

#Feature to Feature Class Using Address Points located in Hope
#Hope Address Points are updated with GeoMAX and are used due to the UNIT_NBR field being populated correctly
inFeature_FTF = "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Owner.sde\\hope.dbo.GeoMAX\\hope.dbo.AddressPTS"
outPath_FTF = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb"
outName_FTF = "AddressPTS_InfoUpdate"

#Keep List is created to have all of the fields needed for the final table
#This list is used in a fieldmappings operation after all of the spatial joins have taken place
KEEP_LIST = ['OBJECTID', 'LOC_ID', 'ST_NUMBER', 'PRE_DIR', 'ST_NAME', 'ST_SUFFIX', 'POST_DIR', 'UNIT_NBR', 'ADDRESS', 'X', 'Y', 'CITY', 'ETJ', 'MUD', 'LANDUSE', 'LEGEND',
'ORDINANCE', 'YEAR', 'Zone_Name', 'DISTRICT', 'RECYCLE', 'WHOLE_DATE', 'VOTING_PREC', 'DRAINDIST', 'SUBDIVISION', 'KEYMAP_LOC', 'PLAT', 'ZIPCODES', 'POSTAL', 'STATE',
'NEIGHBORHOOD', 'COUNTY', 'GREEN_DAY','LONGITUDE', 'LATITUDE', 'ORDINACE__', 'ORDINACE', 'PREC', 'NAME', 'DXF_ATTRIB', 'NAME', "ZIP", "TEXT_", "MUD", "F_ADDRESS", "VicinityArea",
'SUB_CODE', 'hs_exempt', 'size_square_feet', 'yr_built', 'entity_cd', 'PID', 'legal_desc', 'HGAC_AREA']

infoUpdate_path = outPath_FTF +"\\"+ outName_FTF

#Convert prevFeatureCount to String and then Integer to be able to calculate change with each day
#arcpy.GetCount_management is a "Result" and can't be used in a math equation
prevFeatureCount = arcpy.GetCount_management(infoUpdate_path)
prevFeatureCount_str = str(prevFeatureCount)
prevFeatureCount_int = int(prevFeatureCount_str)

#Address Points

arcpy.FeatureClassToFeatureClass_conversion(inFeature_FTF, outPath_FTF, outName_FTF)

inFile.write("Initial Layer Created")
inFile.write("\n")

print ("Address Points done.")


inFile.write("\n----- Spatial Join Section -----")
#City Limit
cityLimit = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.CityLimits"
outFile_cityLimit = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\CityLimitJOIN"


arcpy.SpatialJoin_analysis (infoUpdate_path, cityLimit, outFile_cityLimit)
##n = 0
##BR_lst = [36616, 5566, 5398, 5400, 87808, 16590, 15476, 34502, 5272, 43310, 53928, 74084, 76930, 49648, 15478, 50844]
##fields= ["LOC_ID", "City"]
##for i in BR_lst:
##    with arcpy.da.UpdateCursor(outFile_cityLimit, fields) as Ucur:
##        for Urow in Ucur:
##            if Urow[0] == BR_lst[n]:
##                Urow[1] = "BROOKSIDE VILLAGE"
##                Ucur.updateRow(Urow)
##            else:
##                pass
##    n += 1
print ("City Limit done.")
inFile.write("\nCity Limit Spatial Join Complete...1/19")

#ETJ
etj = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.ETJ"
outFile_etj = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\etjJOIN"

arcpy.SpatialJoin_analysis (outFile_cityLimit, etj, outFile_etj)
print ("ETJ done.")
inFile.write("\nETJ Spatial Join Complete...2/19")

#MUD
mud = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.MUD"
outFile_mud = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\mudJOIN"

arcpy.SpatialJoin_analysis (outFile_etj, mud, outFile_mud)
print ("MUD done.")
inFile.write("\nMUD Spatial Join Complete...3/19")

#FLUP
flup = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.Planning\\cop_sde.DBO.FLUP_2015"
outFile_flup = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\flupJOIN"

arcpy.SpatialJoin_analysis (outFile_mud, flup, outFile_flup)
print ("FLUP done.")
inFile.write("\nFuture Land Use Plan Spatial Join Complete...4/19")

#Ordinance
ordin = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.Ordinance"
outFile_ordin = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\ordinJOIN"

arcpy.SpatialJoin_analysis (outFile_flup, ordin, outFile_ordin)
print ("Ordinance done.")
inFile.write("\nOrdinance Spatial Join Complete...5/19")

#Zoning
zone = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.Planning\\cop_sde.DBO.Zoning"
outFile_zone = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\zoneJOIN"

arcpy.SpatialJoin_analysis (outFile_ordin, zone, outFile_zone)

print ("Zoning done.")
inFile.write("\nZoning Spatial Join Complete...6/19")

#Schools
school = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.Schools\\cop_sde.DBO.School_Districts"
outFile_school = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\schoolJOIN"

arcpy.SpatialJoin_analysis (outFile_zone, school, outFile_school)
print ("Schools done.")
inFile.write("\nSchools Spatial Join Complete...7/19")

#Recycle
rec = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.AdministrativeBoundaries\\Horizon.DBO.Recycle"
outFile_rec = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\recycleJOIN"

arcpy.SpatialJoin_analysis (outFile_school, rec, outFile_rec)
print ("Recycle done.")
inFile.write("\nRecycle Spatial Join Complete...8/19")

#Trash
trash = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.AdministrativeBoundaries\\Horizon.DBO.Trash"
outFile_trash = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\trashJOIN"

arcpy.SpatialJoin_analysis (outFile_rec, trash, outFile_trash)

print ("Trash done.")
inFile.write("\nTrash Spatial Join Complete...9/19")

#Voting
vote = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.VotingPrecinct"
outFile_vote = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\voteJOIN"

arcpy.SpatialJoin_analysis (outFile_trash, vote, outFile_vote)

print ("Voting done.")
inFile.write("\nVoting Spatial Join Complete...10/19")

#HGAC Areas
HGAC = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.HGAC\\cop_sde.DBO.HGAC_AREA_CITIES"
outFile_HGAC = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\HGAC_JOIN"

arcpy.SpatialJoin_analysis (outFile_vote, HGAC, outFile_HGAC)
arcpy.AlterField_management(outFile_HGAC, "NAME", "HGAC_AREA", 'HGAC_AREA')
arcpy.AlterField_management(outFile_HGAC, "STATE", "DELETE", 'DELETE')
inFile.write("\nHGAC SDE Spatial Join Complete...22/19")

#Drainage
drain = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.DrainageDistricts"
outFile_drain = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\drainJOIN"

arcpy.SpatialJoin_analysis (outFile_HGAC, drain, outFile_drain)

print ("Drainage done.")
inFile.write("\nDrainage Spatial Join Complete...11/19")

#Subdivisions
subs = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.Pearland_Subdivisions"
outFile_subs = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\subsJOIN"

arcpy.SpatialJoin_analysis (outFile_drain, subs, outFile_subs)

arcpy.AlterField_management(outFile_subs, "NAME", "SUBDIVISION", "SUBDIVISION")

print ("Subdivision done.")
inFile.write("\nSubdivision Spatial Join Complete...12/19")

#Grid
grid = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.HGAC\\cop_sde.DBO.Pear_KeyMap_letgrid"
outFile_grid = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\gridJOIN"

arcpy.SpatialJoin_analysis (outFile_subs, grid, outFile_grid)

print ("Grid done.")
inFile.write("\nGrid Spatial Join Complete...13/19")

#Plats
plats = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.Planning\\cop_sde.DBO.Plats"
outFile_plats = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\platsJOIN"

arcpy.SpatialJoin_analysis (outFile_grid, plats, outFile_plats)

arcpy.AlterField_management(outFile_plats, "NAME", "PLAT", 'PLAT')

print ("Plats done.")
inFile.write("\nPlats Spatial Join Complete...14/19")

#Zip Code
zipc = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.AdministrativeBoundaries\\Horizon.DBO.ZipCodes"
outFile_zipc = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\zipJOIN"

arcpy.SpatialJoin_analysis (outFile_plats, zipc, outFile_zipc)

inFile.write("\nZip Code Spatial Join Complete...15/19")

#SubSubdivisions
subsub = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.SubSubdivisions"
outFile_subsub = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\subsubJOIN"

arcpy.SpatialJoin_analysis (outFile_zipc, subsub, outFile_subsub)
arcpy.AlterField_management(outFile_subsub, "NAME", "NEIGHBORHOOD", 'NEIGHBORHOOD')
inFile.write("\nSubSubdivisions Spatial Join Complete...16/19")

#County Lines
county = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.County_Lines"
outFile_county = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\countyJOIN"

arcpy.SpatialJoin_analysis (outFile_subsub, county, outFile_county)
inFile.write("\nCounty Lines Spatial Join Complete...17/19")

#Green Waste
green = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AdministrativeBoundaries\\cop_sde.DBO.GreenWaste"
outFile_green = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\gwasteJOIN"

arcpy.SpatialJoin_analysis (outFile_county, green, outFile_green)
inFile.write("\nGreen Waste Spatial Join Complete...18/19")

#Vicinity Area
varea = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER@Hope.sde\\hope.DBO.Dev\\hope.DBO.VicinityArea"
outFile_varea = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\vareaJOIN"

arcpy.SpatialJoin_analysis (outFile_green, varea, outFile_varea)
inFile.write("\nVicinity Area Spatial Join Complete...19/19")

# #Parcels_BCAD_View
# parcel = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Scratch.gdb\\Parcels2019_prelim_bcadjoin"
# outFile_parcel = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\parcelsJOIN"
#
# arcpy.SpatialJoin_analysis (outFile_varea, parcel , outFile_parcel)
# inFile.write("\nParcels BCAD View Spatial Join Complete...20/19")

#Parcels SDE
parcelSDE = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.AppraisalDistricts\\cop_sde.DBO.Parcels2019_Certified"
outFile_parcelSDE = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb\\parcels_sdeJOIN"

arcpy.SpatialJoin_analysis (outFile_varea, parcelSDE, outFile_parcelSDE)
inFile.write("\nParcels SDE Spatial Join Complete...21/19")
print("done1")
inFile.write("\n ")
inFile.write("\n----- Field Mappings Section -----")

#Creating Field mapping
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(outFile_parcelSDE)

#Removing all Fields that aren't needed in the end product
for f in fieldmappings.fields:
        if f.name not in KEEP_LIST:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))

inFile.write("\nRemove Fields Complete")

Table_path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb"
Table_name = "InfoUpdate_FINAL"

Alter_table = Table_path + "\\" + Table_name
arcpy.FeatureClassToFeatureClass_conversion(outFile_parcelSDE, Table_path, Table_name, '', fieldmappings)

#Using Alter Field to change the Field Name for schema purposes
#The Field Name (old is the second parameter, New is the third parameter) is important due to this data being tied into New World and other third parties that rely on the schema remaining the same
#Alias names changes only occur to help the end user bettr understand what the field is
arcpy.AlterField_management(Alter_table, "LEGEND", "LANDUSE")
arcpy.AlterField_management(Alter_table, "ORDINACE__", "ORDINACE", "ORDINANCE")
arcpy.AlterField_management(Alter_table, "YEAR", "ORD_DATE", "ORDINANCE_YEAR")
arcpy.AlterField_management(Alter_table, "Zone_Name", "ZONE", "ZONING")
arcpy.AlterField_management(Alter_table, "DISTRICT", "SCHOOL_DIST", "SCHOOL_DISTRICT")
arcpy.AlterField_management(Alter_table, "RECYCLE", "", "RECYCLE_DAY")
arcpy.AlterField_management(Alter_table, "WHOLE_DATE", "TRASH_DAY", "TRASH_DAY")
arcpy.AlterField_management(Alter_table, "PREC", "VOTING_PREC", "VOTING_PRECINCT")
arcpy.AlterField_management(Alter_table, "DRAINDIST", "DRAINDIST", "DRAINAGE_DISTRICT")
arcpy.AlterField_management(Alter_table, "DXF_ATTRIB", "KEYMAP_LOC", "KEYMAP_LOC")
arcpy.AlterField_management(Alter_table, "ZIP", "ZIPCODES")
arcpy.AlterField_management(Alter_table, "TEXT_", "MUD", 'MUD')
arcpy.AlterField_management(Alter_table, "F_ADDRESS", "ADDRESS", 'ADDRESS')
arcpy.AlterField_management(Alter_table, "GREEN_DAY", "", "GREEN_WASTE_DAY")

inFile.write("\nAlter Fields Complete")

#Grabbing X/Y and LAT/LONG
#INFO TABLE needs both due to different third parties working with different coordinate systems
Table_nameXY = "InfoUpdateLATLONG"
Table_pathXY = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb"

Table_pathLIVE = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\UpdateTableplswork.gdb"
Table_NameLIVE = "InfoUpdateLATLONG_Live"

LDock_path = "\\\\GISAPP\\Workspace\\Models\\Scripts\\GISOWNER@GISDB.sde\\cop_sde.DBO.LoadingDock"
LDock_name = "AddressPts_scripted"

LDock_table = LDock_path + "\\" + LDock_name

XY_table = Table_pathXY + "\\" + Table_nameXY
LIVE_table = Table_pathLIVE + "\\" + Table_NameLIVE

arcpy.Project_management(Alter_table, XY_table, 4269)
arcpy.AddXY_management(XY_table)

inFile.write("\nAdd LAT/LONG (WGS 4326) Complete")

arcpy.AlterField_management(XY_table, "POINT_X", "LONGITUDE")
arcpy.AlterField_management(XY_table, "POINT_Y", "LATITUDE")

arcpy.Project_management(XY_table, LIVE_table, 2278)
arcpy.AddXY_management(LIVE_table)

arcpy.AlterField_management(LIVE_table, "POINT_X", "X", "X")
arcpy.AlterField_management(LIVE_table, "POINT_Y", "Y", "Y")
print("doneXY")
inFile.write("\nAdd XY (State Plane 4204) Complete")

#Creating the official table from InfoUpdateLATLONG_Live located in cschultz Updatetableplswork.gdb
hopeTable_path = "\\\\GISAPP\\Workspace\\Models\\Scripts\\GISOWNER@HOPE_GISDB.sde"
hopeTable_name = "INFO_TABLE_UPDATE"
hopeTable = hopeTable_path + "\\" + hopeTable_name
arcpy.TableToTable_conversion(LIVE_table, hopeTable_path, hopeTable_name)

#Flush and fill the LoadingDock layer to be consumed in map services
arcpy.TruncateTable_management(LDock_table)
arcpy.Append_management(LIVE_table, LDock_table, "NO_TEST")

end = time.time()
elapsed = end - start
elapsed_min = elapsed / 60
elapsed_print = format(elapsed_min, ".2f")
print(elapsed_print)
featureCount = arcpy.GetCount_management(LDock_table)
featureCount_str = str(featureCount)
featureCount_int = int(featureCount_str)


inFile.write("\n")
inFile.write("\nTime Elapsed: "+ str(elapsed_print))
inFile.write("\nProgram Last Ran Date: " + str(datetime.datetime.today().strftime('%Y-%m-%d')))
inFile.write("\nFeature Count: " + str(featureCount))
newFeatureCount = featureCount_int - prevFeatureCount_int
inFile.write("\nFeature Count Change: " + str(newFeatureCount))

msg = MIMEMultipart('alternative')
s = smtplib.SMTP('mail.pearlandtx.gov')

msg['Subject'] = "Info Update Table Updated"
msg['From'] = 'cschultz@pearlandtx.gov'
msg['To'] = 'cschultz@pearlandtx.gov, mmasters@pearlandtx.gov'
msg['X-priority'] = '2'


# Create the body of the message (a plain-text and an HTML version).

html = """\
<html>
  <head></head>
  <body>
    <p>Info Update Table has been updated.<br>
    </p>
  </body>
</html>
"""

text = "The Garage Sale Table has been updated and is ready to be used in this week's report.\n \\COPFS\\City Hall\\Planning\\GarageSaleReports"

### Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(html, 'html')
part2 = MIMEText(text, 'text')
msg.attach(part1)
msg.attach(part2)

s.sendmail(msg['From'], msg['To'].split(","), msg.as_string())

inFile.close()





