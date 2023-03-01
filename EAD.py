# imports
import glob
import sys
import lxml.etree as etree

# namespace declarations
class XMLNamespaces:
   xlink = 'http://www.w3.org/1999/xlink'
   ead = "urn:isbn:1-931666-22-9"

# register namespaces into etree
etree.register_namespace("ead", XMLNamespaces.ead)
etree.register_namespace("xlink", XMLNamespaces.xlink)

# get dir from sys argument
rootdir = sys.argv[1]

# root_dir needs a trailing slash (i.e. /root/dir/)
for filename in glob.iglob(rootdir + '**/*.xml', recursive=True):
    print(filename)
    # read all mets files
    el = etree.parse(filename)

    # find default filegroup for copying values
    files = el.findall("//ead:daoloc, namespaces = {"ead": "urn:isbn:1-931666-22-9"})  
    
    i = 0
    # iterate over all file entries
    for file in files:


        # build new daoloc element and fill content from DEFAULT
        elementGrp = etree.Element(etree.QName("urn:isbn:1-931666-22-9", "daoloc"))

        elementGrp.attrib["xlink:role"] = "METS"
        elementGrp.attrib["xlink:href"] = file.attrib["xlink:href"]

        parent = file.parent()
        parent.append(elementGrp)
        parent.remove(file)
    

        i = i + 1

    #print(etree.tostring(el, pretty_print=False))
    #etree.ElementTree(el).write('D:\test.xml', pretty_print=True)
    print("Changing file: ", filename)
    with open(filename, 'wb') as f:
        el.write(f, encoding='UTF-8')