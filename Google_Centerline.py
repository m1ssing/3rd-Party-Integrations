import arcpy
import os
import time

start = time.time()
arcpy.env.overwriteOutput = True



inFeature_FTF = "\\\\GISAPP\\Workspace\\sdeFiles\\GISVIEWER_GISDB.sde\\cop_sde.DBO.Transportation\\cop_sde.DBO.Centerline_Master"
outPath_FTF = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb"
outName_FTF = "Centerline"

layer_path = outPath_FTF + "\\" + outName_FTF
KEEP_LIST = ["ID", "ST_NAME", "AR_LT_FR", "AR_LT_TO", "AR_RT_FR", "AR_RT_TO" ]



arcpy.FeatureClassToFeatureClass_conversion(inFeature_FTF, outPath_FTF, outName_FTF)

arcpy.AddField_management(layer_path, "CITY", "TEXT")
arcpy.AddField_management(layer_path, "STATE", "TEXT")

arcpy.AlterField_management(layer_path, "CNTLN_ID", "ID", "ID")
arcpy.AlterField_management(layer_path, "INDEX_NAME", "ST_NAME","ST_NAME")
arcpy.AlterField_management(layer_path, "L_ADD_FROM", "AR_LT_FR", "AR_LT_FR")
arcpy.AlterField_management(layer_path, "L_ADD_TO", "AR_LT_TO", "AR_LT_TO")
arcpy.AlterField_management(layer_path, "R_ADD_TO", "AR_RT_FR", "AR_RT_FR")
arcpy.AlterField_management(layer_path, "R_ADD_FROM", "AR_RT_TO", "AR_RT_TO")
fields = ["CITY", "STATE"]
with arcpy.da.UpdateCursor(layer_path, fields ) as Ucur:
    for row in Ucur:
        row[0] = "Pearland"
        row[1] = "TX"
        Ucur.updateRow(row)

fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(layer_path)

for f in fieldmappings.fields:
    if f.name not in KEEP_LIST:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))

Table_path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb"
Table_name = "Centerline_NoClip"   
Centerline_path = Table_path + "\\" + Table_name
arcpy.FeatureClassToFeatureClass_conversion(layer_path, Table_path, Table_name, "", fieldmappings)

Table_name_clip = "Centerline_Clip"   
CenterlineClip_path = Table_path + "\\" + Table_name_clip
CityBoundary = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb\\CityBoundaries_Buffer"
arcpy.Clip_analysis(Centerline_path, CityBoundary, CenterlineClip_path )

print(".")