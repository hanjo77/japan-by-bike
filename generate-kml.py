import os
import re
import xml.etree.ElementTree as ElementTree 

def handle_error(errorMsg, file, e):
	print (errorMsg)

def log(msg, file):
	print (msg)

baseFileName = "japan-by-bike.kml"

def get_coordinates(file):
    if not os.path.isfile(file):
        handle_error("File '%s' does not exist.", file)
    try:
        tree = ElementTree.parse(file)
    except e:
        handle_error("Table file %s is invalid: %s", file, e)
	
    root = tree.getroot()
    for elem in root.getchildren()[0].getchildren():
        if elem.tag.find("Placemark") > -1:
            for subelem in elem.getchildren():
                if subelem.tag.find("LineString") > -1:
                    for subsubelem in subelem.getchildren():
                        if subsubelem.tag.find("coordinates") and len(subsubelem.text) > 100:
                            return subsubelem.text

    return ""

coordinates = ""

for subdir, dirs, files in os.walk('./'):
    files.sort()
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext == ".xml":
            coordinates += get_coordinates(file)

coordinates = re.sub("\n\s*\n", "\n", coordinates)

with open(baseFileName) as f:
    newText=re.sub("<coordinates>[^<]*</coordinates>", "<coordinates>" + coordinates + "</coordinates>", f.read())

with open(baseFileName, "w") as f:
    f.write(newText)

## print get_coordinates("01 wakkanai to nakagawa.xml")