#! /usr/bin/env python
#coding=utf-8


import os
from xml.etree.ElementTree import ElementTree


class anrpDefinitionInfoClass:
    def __init__(self, packageName = None):
        if packageName == None:
            self.packageName = ''
        else:
            self.packageName = packageName
        self.type = ''
        self.resSourceList = []
        return

    def LoadXml(self, xmlFilename = None, anrpBaseDirStr = None):
        #生成 XML 文件的绝对路径
        if xmlFilename == None:
            xmlFilename = self.packageName
        xmlFilename = '%s.anrp.rpd.xml' % xmlFilename
        if anrpBaseDirStr != None:
            xmlFilename = os.path.join(anrpBaseDirStr, xmlFilename)

        tree = ElementTree()
        tree.parse(xmlFilename)

        resPackageDefinedRoot = tree.getroot()

        self.packageName = resPackageDefinedRoot.find('packageName').text
        self.type = resPackageDefinedRoot.find('type').text

        self.resSourceList = []
        for resSourceX in resPackageDefinedRoot.findall('resSourceList'):
            resSourceDict = {}
            if anrpBaseDirStr == None:
                resSourceDict['resPath'] = resSourceX.get('resClass')
            else:
                resSourceDict['resPath'] = os.path.join(anrpBaseDirStr, resSourceX.get('resClass'))
            resSourceDict['resName'] = resSourceX.get('resId')

            self.resSourceList.append(resSourceDict)

        return

    def PrintInfo(self):
        print 'self.packageName:', self.packageName
        print 'self.type:', self.type
        print 'self.resSourceList:', self.resSourceList
        return


if '__main__' == __name__:
    anrpDefObj = anrpDefinitionInfoClass('man')
    anrpDefObj.LoadXml(anrpBaseDirStr='C:\\Coding\\sm_Trunk\\res\\resPackage')
    anrpDefObj.PrintInfo()