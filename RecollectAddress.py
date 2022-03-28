import arcpy
arcpy.env.overwriteOutput = True

ServiceType = "\\\\GISAPP\\Workspace\\sdeFiles\\GISOWNER_GISDB.sde\\cop_sde.DBO.GeoMax\\cop_sde.DBO.NW_ActiveSeviceType"
AddressPTS = "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Owner.sde\\hope.DBO.GeoMAX\\hope.DBO.AddressPTS"

arcpy.FeatureClassToFeatureClass_conversion(ServiceType, "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb", "ServiceType", "ServiceTypes LIKE '%RES GARBAGE%'")
arcpy.FeatureClassToFeatureClass_conversion(AddressPTS, "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb", "AddressPTS")

Recollect_ServiceType = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb\\ServiceType"
Recollect_AddressPTS = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb\\AddressPTS"
arcpy.management.AddField(Recollect_AddressPTS, "AddressUnit", "TEXT")
arcpy.management.CalculateField(Recollect_AddressPTS, "AddressUnit", "AddressCalc(!F_ADDRESS!,!UNIT_NBR!)", "PYTHON3", """def AddressCalc(address, unit):
    if unit == "":
        return(address)
    if unit != "":
        return(address + " " + unit)""", "TEXT", "NO_ENFORCE_DOMAINS")
join = arcpy.AddJoin_management(Recollect_ServiceType, "AddressLine1", Recollect_AddressPTS, "AddressUnit")
arcpy.FeatureClassToFeatureClass_conversion(join, "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb", "AddressJOIN")
Recollect_Join = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb\\AddressJOIN"

arcpy.management.AlterField(Recollect_Join, "F_ADDRESS", "AddressNoUnit")
arcpy.management.AlterField(Recollect_Join, "AddressUnit", "F_ADDRESS", "F_ADDRESS")

KEEP_LIST = ["ST_NUMBER", "PRE_DIR", "ST_NAME", "ST_SUFFIX", "POST_DIR", "UNIT_NBR", "F_ADDRESS", "ServiceTypes"]
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(Recollect_Join)

for f in fieldmappings.fields:
    if f.name not in KEEP_LIST:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(f.name))
arcpy.conversion.FeatureClassToFeatureClass(Recollect_Join, "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb", "AddressFINAL", "", fieldmappings)
addressImport = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\Recollect.gdb\\AddressFINAL"
arcpy.management.DeleteIdentical(addressImport, "F_ADDRESS")
HopeLayer = "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Owner.sde\\hope.DBO.GeoMAX\\hope.DBO.Recollect_TrashAddress"

if arcpy.Exists(HopeLayer) == False:
    arcpy.FeatureClassToFeatureClass_conversion(addressImport, "\\\\GISAPP\\Workspace\\sdeFiles\\Hope_Owner.sde\\hope.DBO.GeoMAX", "Recollect_TrashAddress")

arcpy.TruncateTable_management(HopeLayer)
arcpy.Append_management(addressImport, HopeLayer)


print(".")

