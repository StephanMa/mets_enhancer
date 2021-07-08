# imports
import glob
import sys
import lxml.etree as etree

# namespace declarations
class XMLNamespaces:
   xlink = 'http://www.w3.org/1999/xlink'
   mets = "http://www.loc.gov/METS/"

# register namespaces into etree
etree.register_namespace("mets", XMLNamespaces.mets)
etree.register_namespace("xlink", XMLNamespaces.xlink)

# get dir from sys argument
rootdir = sys.argv[1]

# root_dir needs a trailing slash (i.e. /root/dir/)
for filename in glob.iglob(rootdir + '**/mets.xml', recursive=True):
    print(filename)
    # read all mets files
    el = etree.parse(filename)

    # find default filegroup for copying values
    files = el.findall("//mets:fileGrp[@USE='DEFAULT']/mets:file", namespaces = {"mets": "http://www.loc.gov/METS/"})  

    # create initial download filegroup 
    elementGrp = etree.Element(etree.QName("http://www.loc.gov/METS/", "fileGrp"))
    elementGrp.attrib["USE"] = "DOWNLOAD"
    
    i = 0
    # iterate over all file entries
    for file in files:

        # split IDs for building ID String 
        ids_split = str(file.attrib["ID"]).split("_")
        id_dl = ids_split[0] + "_" + ids_split[1]

        # build file element and fill content from DEFAULT
        elementFile = etree.SubElement(elementGrp, etree.QName("http://www.loc.gov/METS/", "file"), {"ID": "", "MIMETYPE": "", "SIZE": ""})
        elementFile.attrib["ID"] = id_dl + "_DLT"
        elementFile.attrib["MIMETYPE"] = file.attrib["MIMETYPE"]
        elementFile.attrib["SIZE"] = file.attrib["SIZE"]

        # build FLocat 
        elementFLocat = etree.SubElement(elementFile, etree.QName(XMLNamespaces.mets, "FLocat"), {"LOCTYPE": "", etree.QName(XMLNamespaces.xlink, "href"): ""})
        elementFLocat.attrib["LOCTYPE"] = "URL"
        elementFLocat.attrib[etree.QName(XMLNamespaces.xlink, "href")] = file.find("{http://www.loc.gov/METS/}FLocat").attrib[etree.QName(XMLNamespaces.xlink, "href")]

        # build filepointer
        id = "ID_" + ids_split[1]
        f_id = "FID_" + ids_split[1] + "_DLT"
        
        fptr = el.findall("//mets:div[@TYPE='page']", namespaces = {"mets": "http://www.loc.gov/METS/"})  

        elementFptr = etree.SubElement(fptr[i], etree.QName(XMLNamespaces.mets, "fptr"), {"FILEID": f_id})

        fptr[i].append(elementFptr)

        i = i + 1

    # print(etree.tostring(elementGrp))

    # add filegroup DOWNLOAD to file
    fileSec = el.find(".//mets:fileSec", namespaces = {"mets": "http://www.loc.gov/METS/"})  

    # write file
    fileSec[0].getparent().append(elementGrp)

    #print(etree.tostring(el, pretty_print=False))
    #etree.ElementTree(el).write('D:\test.xml', pretty_print=True)
    with open(filename, 'wb') as f:
        el.write(f, encoding='UTF-8')