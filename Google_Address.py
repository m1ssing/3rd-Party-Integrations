import arcpy

arcpy.env.overwriteOutput = True



inFeature_FTF = "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Viewer.sde\\hope.dbo.GeoMAX\\hope.DBO.AddressPTS"
outPath_FTF = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb"
outName_FTF = "Address"

layer_path = outPath_FTF + "\\" + outName_FTF
KEEP_LIST = ["ZIP", "ST_NUMBER", "Street_Name", "CITY", "State"]



arcpy.FeatureClassToFeatureClass_conversion(inFeature_FTF, outPath_FTF, outName_FTF)

arcpy.AddField_management(layer_path, "CITY", "TEXT")
arcpy.AddField_management(layer_path, "Street_Name", "TEXT")

fields = ["CITY"]
with arcpy.da.UpdateCursor(layer_path, fields ) as Ucur:
    for row in Ucur:
        row[0] = "Pearland"
        Ucur.updateRow(row)
fields_st = ["Street_Name", "PRE_DIR", "ST_NAME", "ST_SUFFIX"]
with arcpy.da.UpdateCursor(layer_path, fields_st ) as Ucur:
    for row in Ucur:
        if row[1] != "":
            row[0] = row[1]+ " " + row[2] + " " + row[3]
            Ucur.updateRow(row)
        else:
            row[0] =  row[2] + " " + row[3]
            Ucur.updateRow(row)

address_layer = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb\\AddressSpatialJoin"
ZIP = "\\\\GISAPP\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.AdministrativeBoundaries\\Horizon.DBO.ZipCodes"
arcpy.SpatialJoin_analysis(layer_path, ZIP, address_layer )
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(address_layer)

for f in fieldmappings.fields:
    if f.name not in KEEP_LIST:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))

Table_path = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Google.gdb"
Table_name = "Address_Clip"   
Centerline_path = Table_path + "\\" + Table_name
arcpy.FeatureClassToFeatureClass_conversion(address_layer, Table_path, Table_name, "", fieldmappings)
arcpy.AlterField_management(Centerline_path, "Street_Name", "ST_NAME", "ST_NAME")
arcpy.AlterField_management(Centerline_path, "ST_NUMBER", "ST_NUM", "ST_NUM")

print(".")