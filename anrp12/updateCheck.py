#! /usr/bin/env python
#coding=utf-8


import os
from xml.etree.ElementTree import ElementTree


def GetFileLastModifyTime(fullPathFilename):
    """获取文件最后修改时间"""
    fileStats = os.stat(fullPathFilename)

    lastMofiyTime = fileStats.st_mtime
    return lastMofiyTime

def IsNeedUpdate(srcFile, dstfile):#还缺乏对文件大小的对比!!!!!!!!!
    """根据文件最后修改时间判断文件是否需要更新"""
    try:
        srcFileTime = GetFileLastModifyTime(srcFile)
        dstfileTime = GetFileLastModifyTime(dstfile)
        if srcFileTime < dstfileTime:
            return False
    except:
        #print '!!!\n'
        pass

    return True


def IsNeedUpdate4AtxXml(atxPackageName, atxResBaseDir, atxFileDir):
    atxRpdFileFullPath = os.path.join(atxResBaseDir, '%s.xml' % atxPackageName) #ATX资源定义文件名
    atxOutputFilePullPath = os.path.join(atxFileDir, '%s.anrp' % atxPackageName) #生成的 anrp 文件名
    resFilePath = os.path.join(atxResBaseDir, atxPackageName)

    #解析 XML 文件，生成需要检测的文件清单
    if IsNeedUpdate(atxRpdFileFullPath, atxOutputFilePullPath):
        #ATX资源定义文件已经更新
        return True

    #获取图片文件清单
    fileFullnameList = []
    for path, dirs, files in os.walk(resFilePath):
        for filenameX in files:
            fileFullnameList.append(os.path.join(path, filenameX))

    #逐一比对
    for filenameX in fileFullnameList:
        if IsNeedUpdate(filenameX, atxOutputFilePullPath):
            #资源定义文件已经更新
            return True

    return False