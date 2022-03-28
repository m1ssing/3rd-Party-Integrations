import arcpy
import os
import time

start = time.time()
arcpy.env.overwriteOutput = True

logFile = open("\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\PythonFiles\\InfoUpdateTable_log_new.txt", "w")

inFeature_FTF = "\\\\GISAPP\\Workspace\\Models\\Scripts\\GISOWNER@HOPE_GISDB.sde\\hope.DBO.GeoMAX\\hope.DBO.AddressPTS"
outPath_FTF = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb"
outName_FTF = "AddressPTS_InfoUpdate"

infoUpdate_path = outPath_FTF + "\\" + outName_FTF

arcpy.FeatureClassToFeatureClass_conversion(inFeature_FTF, outPath_FTF, outName_FTF)
#Removed GreenWaste (10/01/2021) due to GReen Waste Day being the same as TRash due to Frontier contract

KEEP_LIST = ["OBJECTID", "LOC_ID", "ST_NUMBER", "PRE_DIR", "ST_NAME", "ST_SUFFIX", "POST_DIR", "UNIT_NBR", "ADDRESS", "CITY", "ETJ", "MUD", "LandUsePlan", "Ordinance", "Ord_Year", "Zone_Name", "Zone_Description", "SchoolDistrict",
             "RECYCLE", "TrashDay", "PRECINCT", "CityName", "DrainageDistrict", "Neighborhood", "Neighborhood_Code", "KeyMapLocation", "PlatName", "ZIP_CODE", "Postal", "State", "Name", "COUNTY",
             "VicinityArea", "PID", "legal_desc", "yr_built", "entity_cd", "sq_feet", "hs_exempt", "FloodZone", "land_state_cd", "AppraisedValue", "ImpValue" ]


#Dictionary Format {Name:[Feature Dataset (str), Feature Layer Name (str), outFile_Name (str), Previous outFile_Name (str)]}
dict = {"CityLimit": ["AdministrativeBoundaries", "CityLimits", "outFile_CityBoundaries", "AddressPTS_InfoUpdate"],        
        "MUD": ["AdministrativeBoundaries", "MUD", "outFile_MUD", "outFile_CityBoundaries"],
        "FutureLandUsePlan": ["Planning", "FLUP_2015", "outFile_FLUP", "outFile_MUD"],
        "Ordinance": ["AdministrativeBoundaries", "Ordinance", "outFile_Ordinance", "outFile_FLUP"],
        "Zoning": ["Planning", "Zoning", "outFile_Zoning", "outFile_Ordinance"],
        "SchoolDistricts": ["Schools", "SchoolDistricts", "outFile_Schools", "outFile_Zoning"],
        "Recycle": ["AdministrativeBoundaries", "Recycle", "outFile_Recycle", "outFile_Schools"],
        "Trash": ["AdministrativeBoundaries", "Trash", "outFile_Trash", "outFile_Recycle"],
        "Voting": ["AdministrativeBoundaries", "VotingPrecincts", "outFile_Voting", "outFile_Trash"],
        "HGAC": ["HGAC", "HGACAreaCities", "outFile_HGAC", "outFile_Voting"],
        "Drainage": ["AdministrativeBoundaries", "DrainageDistricts", "outFile_Drainage", "outFile_HGAC"],
        "Neighborhoods": ["AdministrativeBoundaries", "Neighborhoods", "outFile_Neighborhoods", "outFile_Drainage"],
        "Grid": ["HGAC", "KeyMapGrid", "outFile_Grid", "outFile_Neighborhoods"],
        "Plats": ["Planning", "Plats", "outFile_Plats", "outFile_Grid"],
        "ZIP": ["AdministrativeBoundaries", "ZipCodes", "outFile_ZIP", "outFile_Plats"],
        "Subdivision": ["InfoUpdate", "Subdivisions", "outFile_Subs", "outFile_ZIP"],
        "Counties": ["AdministrativeBoundaries", "Counties", "outFile_County", "outFile_Subs"],
        "GreenWaste": ["AdministrativeBoundaries", "GreenWaste", "outFile_Green", "outFile_County"],
        "VicinityArea": ["InfoUpdate", "VicinityArea", "outFile_Vicinity", "outFile_Green"],
        "Parcels": ["AppraisalDistricts", "Parcels2020_Certified", "outFile_Parcels", "outFile_Vicinity"],
        "FEMA":["FEMA", "Brazoria_FloodPlain", "outFile_FEMA", "outFile_Parcels"],
        "ParkZone":["ParksRec", "ParkZones", "outFile_Parks", "outFile_FEMA"],
        "ETJ": ["AdministrativeBoundaries", "CityETJ", "outFile_ETJ", "outFile_Parks"]}

logFile.write("Initial Layer Created.\n")
logFile.write("\n")
logFile.write("----- Spatial Join Section -----\n")

n = 1
m = len(dict)
for key,value in dict.items():
    oldtable = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb\\{}".format(value[3])
    inFile = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.{}\\Horizon.DBO.{}".format(value[0], value[1])
    outFile = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb\\{}".format(value[2])
    print("{} done.".format(value[2]))

    arcpy.SpatialJoin_analysis(oldtable, inFile, outFile)
    logFile.write("{} complete...{}/{}\n".format(value[2], n, m))
    n += 1

arcpy.AddField_management(outFile, "FloodZone", "TEXT")
fields = ["FEMA_ID", "FloodZone"]

with arcpy.da.UpdateCursor(outFile, fields) as cursor:
    for row in cursor:
        if row[0] == 0:
            row[1] = "YES"
            cursor.updateRow(row)
        else:
            row[1] = "NO"
            cursor.updateRow(row)

fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(outFile)

for f in fieldmappings.fields:
    if f.name not in KEEP_LIST:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))



Table_path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb"
Table_name = "InfoUpdate_FINAL"
notXY_table = Table_path + "\\" + Table_name

arcpy.FeatureClassToFeatureClass_conversion(outFile, Table_path, Table_name, '', fieldmappings)

arcpy.management.AlterField(notXY_table, "LandUsePlan", "LANDUSE", "LANDUSE")
arcpy.management.AlterField(notXY_table, "Ordinance", "ORDINACE", "ORDINANCE")
arcpy.management.AlterField(notXY_table, "Ord_Year", "ORD_DATE", "ORDINANCE_YEAR")
arcpy.management.AlterField(notXY_table, "Zone_Name", "ZONE", "ZONING")
arcpy.management.AlterField(notXY_table, "SchoolDistrict", "SCHOOL_DIST", "SCHOOL_DISTRICT")
arcpy.management.AlterField(notXY_table, "RECYCLE", "", "RECYCLE_DAY")
arcpy.management.AlterField(notXY_table, "TrashDay", "TRASH_DAY", "TRASH_DAY")
arcpy.management.AlterField(notXY_table, "PRECINCT", "VOTING_PREC", "VOTING_PRECINCT")
arcpy.management.AlterField(notXY_table, "CityName", "HGAC_AREA", "HGAC_AREA")
arcpy.management.AlterField(notXY_table, "DrainageDistrict", "DRAINDIST", "DRAINAGE_DISTRICT")
arcpy.management.AlterField(notXY_table, "Neighborhood", "SUBDIVISION", "SUBDIVISION")
arcpy.management.AlterField(notXY_table, "KeyMapLocation", "KEYMAP_LOC", "KEYMAP_LOC")
arcpy.management.AlterField(notXY_table, "PlatName", "PLAT", "PLAT")
arcpy.management.AlterField(notXY_table, "ZIP_CODE", "ZIPCODES", "ZIP")
arcpy.management.AlterField(notXY_table, "Name", "NEIGHBORHOOD", "NEIGHBORHOOD")

# Grabbing X/Y and LAT/LONG
# INFO TABLE needs both due to different third parties working with different coordinate systems
Table_nameXY = "InfoUpdateLATLONG"
Table_pathXY = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb"

Table_pathLIVE = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\InfoUpdate.gdb"
Table_NameLIVE = "InfoUpdateLATLONG_Live"

# LDock_path = "\\\\GISAPP\\Workspace\\Models\\Scripts\\GISOWNER@GISDB.sde\\cop_sde.DBO.LoadingDock"
# LDock_name = "AddressPts_scripted"
#
# LDock_table = LDock_path + "\\" + LDock_name

XY_table = Table_pathXY + "\\" + Table_nameXY
LIVE_table = Table_pathLIVE + "\\" + Table_NameLIVE

arcpy.Project_management(notXY_table, XY_table, 4269)
arcpy.AddXY_management(XY_table)

logFile.write("\nAdd LAT/LONG (WGS 4326) Complete")

arcpy.AlterField_management(XY_table, "POINT_X", "LONGITUDE", "LONGITUDE")
arcpy.AlterField_management(XY_table, "POINT_Y", "LATITUDE", "LATITUDE")

arcpy.Project_management(XY_table, LIVE_table, 2278)
arcpy.AddXY_management(LIVE_table)

arcpy.AlterField_management(LIVE_table, "POINT_X", "X", "X")
arcpy.AlterField_management(LIVE_table, "POINT_Y", "Y", "Y")

end = time.time()
elapsed = end - start
elapsed_min = elapsed / 60
logFile.write("\n{:.2f} minutes".format(elapsed_min))
logFile.close()


#Creating the official table from InfoUpdateLATLONG_Live located in cschultz Updatetableplswork.gdb
hopeTable_path = "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Owner.sde"
hopeTable_name = "INFO_TABLE_UPDATE_REDUX"
hopeTable = hopeTable_path + "\\" + hopeTable_name
arcpy.TableToTable_conversion(LIVE_table, hopeTable_path, hopeTable_name)


##Creating the official table from InfoUpdateLATLONG_Live located in cschultz Updatetableplswork.gdb
#horizonTable_path = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Owner.sde"
#horizonTable_name = "INFO_TABLE_UPDATE"
#hopeTable = horizonTable_path + "\\" + horizonTable_name
#arcpy.TableToTable_conversion(LIVE_table, horizonTable_path, horizonTable_name)

print(".")