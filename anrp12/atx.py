#! /usr/bin/env python
#coding=utf-8


import os
from xml.etree.ElementTree import ElementTree
import multiprocessing

import imageProcess


lock = multiprocessing.Lock()
def DoCutImage(resImageIndex, imageFilenameX, atxBaseDirStr, resTitlePy):
    if atxBaseDirStr != None:
        imageFileDir, imageFileName = os.path.split(imageFilenameX)
        imageFilenameX = os.path.join(atxBaseDirStr, imageFileDir, imageFileName)

    imageProcessObj = imageProcess.imageProcess()
    imageProcessObj.OpenPNG(imageFilenameX)
    iWidth, iHeight = imageProcessObj.imageObj.size
    cutedImageObj = imageProcessObj.CutBlackBorder()
    cutedImageData = imageProcessObj.GetRGB555Data()

    resCutedWidth, resCutedHeight = cutedImageObj.size

##    #根据图片动态计算 resTitlePy
##    resCutedTop = imageProcessObj.cutTop
##    resTitlePy = resCutedTop - 5

##    #根据 resCutedTop 计算出 resTitlePy
##    resCutedTop = imageProcessObj.cutTop
##    resTitlePy = 0
##    if resCutedTop >= 40:
##        resTitlePy = 40
##    if resCutedTop >= 45:
##        resTitlePy = 40
##    if resCutedTop >= 70:
##        resTitlePy = 65
##    if resCutedTop >= 95:
##        resTitlePy = 90
##    if resCutedTop >= 115:
##        resTitlePy = 110

    imageHeaderAndDataDict = {
        'resImageIndex' : resImageIndex,
        'resSize' : len(cutedImageData), #RGB555
        'resTitlePy' : resTitlePy,
        'resCutedLeft' : imageProcessObj.cutLeft,
        'resCutedTop' : imageProcessObj.cutTop,
        'resCutedWidth' : resCutedWidth,
        'resCutedHeight' : resCutedHeight,
        'cutedImageData' : cutedImageData,
    }

    global lock
    lock.acquire()
    ##print '%s' % resImageIndex
    if imageProcessObj.isBlackImage:
        print '%s' % resImageIndex,
    else:
        print '.',
    lock.release()

    return imageHeaderAndDataDict


class atxClass:
    def __init__(self, atxName = None):
        self.name = atxName
        self.iWidth = 0
        self.iHeight = 0
        self.resTitlePy = 0
        self.subResCount = 0
        self.imageFileDir = ''
        self.imageFilenameList = []
        return

    def ReadFromXml(self, atxName = None, atxBaseDirStr = None):
        if atxName != None:
            self.name = atxName

        print "atx.ReadFromXml('%s', '%s')" % (atxName, atxBaseDirStr)
        #解析 XML 文件
        tree = ElementTree()
        atxXmlFilename = '%s.xml' % self.name
        if atxBaseDirStr != None:
            atxXmlFilename = os.path.join(atxBaseDirStr, atxXmlFilename)
        tree.parse(atxXmlFilename)

        resSourceRoot = tree.getroot()
        type = resSourceRoot.find('type').text
        imageFileName = resSourceRoot.find('imageFileName').text

        self.iWidth = int(resSourceRoot.find('iWidth').text)
        self.iHeight = int(resSourceRoot.find('iHeight').text)

        if resSourceRoot.find('titlePy') != None:
            #如果定义文件中有这个值就是用
            self.resTitlePy = int(resSourceRoot.find('titlePy').text)
        else:
            #如果没有就使用默认的值
            self.resTitlePy = 0

        self.subResCount = int(resSourceRoot.find('subResCount').text)
        for x in range(self.subResCount):
            self.imageFilenameList.append('%s-%d.png' % (imageFileName, x+1))

        return

    def GetOneAtxData(self, atxResName, atxBaseDirStr = None):
        '''获取一个 ATX 资源包的所有数据，并且存放在 self.* 里面。未来可能会添加返回的状态值，现在无'''

        #读取 ATX 源数据的 XML 定义文件
        self.ReadFromXml(atxResName, atxBaseDirStr)
        
        anHeaderDict = {
            'resAnIndex' : 1,#填默认值 1
            'resName' : atxResName,
            'resAnGroupAmount' : self.subResCount,
            'resWidth' : self.iWidth,
            'resHeight' : self.iHeight,
        }
        self.packageAnHeaderList = []
        self.packageAnHeaderList.append(anHeaderDict)

        #读取图片数据
        resImageIndex = 1
        mpPool = multiprocessing.Pool(processes=4) #4个子进程
        cutedImageInfoList = []
        if len(self.imageFilenameList) != self.subResCount:
            #异常!!!!!!!!!!!
            raise
        for imageFilenameX in self.imageFilenameList:
            #自动切黑边
            cutedImageInfoList.append(mpPool.apply_async(DoCutImage, (resImageIndex, imageFilenameX, atxBaseDirStr, self.resTitlePy)))
            resImageIndex += 1
        mpPool.close()
        mpPool.join()

        self.packageImageHeaderList = []
        self.packageImageDatalist = []
        for x in range(len(self.imageFilenameList)):
            #整理，然后保存数据
            imageHeaderAndDataDict = cutedImageInfoList[x].get()
            cutedImageData = imageHeaderAndDataDict['cutedImageData']
            del imageHeaderAndDataDict['cutedImageData']

            self.packageImageHeaderList.append(imageHeaderAndDataDict)
            self.packageImageDatalist.append(cutedImageData)

        return





if '__main__' == __name__:
    atxObj = atxClass()

    atxName = 'jwml302'
    #atxObj.ReadFromXml(atxName)
   # print atxObj.iWidth, atxObj.iHeight, atxObj.subResCount

    atxBaseDirStr = 'C:\\Users\\ZLove\\Desktop\\anrp'
    #atxObj.ReadFromXml(atxName, atxBaseDirStr)
    #print atxObj.iWidth, atxObj.iHeight, atxObj.subResCount

    atxResName = 'jwml302'
    import time
    startTime = time.time()
    atxObj.GetOneAtxData(atxResName,atxBaseDirStr)
    print time.time() - startTime
