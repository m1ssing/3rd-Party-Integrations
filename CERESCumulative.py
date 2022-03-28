import arcpy

currentTable = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\scratch.gdb\\CERESData"
cumulativeTable = "\\\\GISAPP\\Workspace\\GIS Staff Workspace\\cschultz\\CERESCumulative"

currentFields = ["Disposal", "Amount"]
currentDict = {}

with arcpy.da.SearchCursor(currentTable, currentFields) as Scur:
    for row in Scur:
        currentDict[row[0]] = []

with arcpy.da.SearchCursor(currentTable, currentFields) as Scur:
    for row in Scur:
        for key,value in currentDict.items():
            if row[0] == key:
                currentDict[row[0]].append(row[1])
lst = []

for key,value in currentDict.items():
    print(key, sum(value))
    lst.append(sum(value))
    print(sum(lst))
print(sum(lst))
print(".")
del currentTable
del cumulativeTable
