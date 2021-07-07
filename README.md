# mets_enhancer

Aufruf des Skripts per
`C:/Python39/python.exe d:/Arbeit/Python_METS/METS.py D:\` 

Der erste Befehlszeilenparameter gibt das Verzeichnis an was durchsucht werden soll.
Es werden rekursiv alle Unterordner dezidiert nach "mets.xml" gecheckt und diese Dateien verarbeitet.
Hierfür wird die `<fileGrp use="DEFAULT">` kopiert und nach `<fileGrp use="DOWNLOAD">` überführt.
