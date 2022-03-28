import arcpy
arcpy.env.overwriteOutput = True

addrLayer = "\\\\gisapp\\Workspace\\sdeFiles\\hope_viewer.sde\\hope.DBO.GeoMax\\hope.DBO.AddressPTS"
newPath = "\\\\gisapp\\Workspace\\GIS Staff Workspace\\cschultz\\PerfectMind.gdb"
newName = "AddressPTS"
joinLayer = "\\\\gisapp\\Workspace\\GIS Staff Workspace\\cschultz\\PerfectMind.gdb\\SpatialJoin"
newLayer = newPath + "\\" + newName
zipLayer = "\\\\gisapp\\Workspace\\sdeFiles\\Horizon_Viewer.sde\\Horizon.DBO.AdministrativeBoundaries\\Horizon.DBO.ZipCodes"
if arcpy.Exists(newLayer):
    arcpy.Delete_management(newLayer)
    arcpy.FeatureClassToFeatureClass_conversion(addrLayer, newPath, newName)
else:
    arcpy.FeatureClassToFeatureClass_conversion(addrLayer, newPath, newName)

#Field Map just ZIP and then add city and state with field calc instead
if arcpy.Exists(joinLayer):
    arcpy.SpatialJoin_analysis(newLayer, zipLayer, joinLayer)
else:
    arcpy.SpatialJoin_analysis(newLayer, zipLayer, joinLayer)


fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(joinLayer)
KEEP_LIST = ["ObjectID", "LOC_ID", "ST_NUMBER", "PRE_DIR", "ST_NAME", "ST_SUFFIX", "POST_DIR", "ST_APT_NBR", "F_ADDRESS", "ZIP"]

for f in fieldmappings.fields:
    if f.name not in KEEP_LIST:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))

finalLayer = "\\\\gisapp\\Workspace\\GIS Staff Workspace\\cschultz\\PerfectMind.gdb\\GeocodeLayer"
finalName = "GeocodeLayer"
arcpy.FeatureClassToFeatureClass_conversion(joinLayer, newPath, finalName, "", fieldmappings)


arcpy.AddField_management(finalLayer, "State", "TEXT")
arcpy.AddField_management(finalLayer, "City", "TEXT")
arcpy.CalculateField_management(finalLayer, "State", "'TX'")
arcpy.CalculateField_management(finalLayer, "City", "'Pearland'")

arcpy.conversion.FeatureClassToFeatureClass()
print(".")