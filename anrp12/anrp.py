#! /usr/bin/env python
#coding=utf-8

'''
AnRP Header and Data

会生成两种格式文件
    *.arph 动画图片资源的定义头
    *.arpd 动画图片资源的数据

或者生成整合成一个文件的格式
    *.anrp
'''


''' AnRPH
包标识区
+-------------------------------------------------------------------------------+
|                                       8                                       |
+-------------------+-------------------+-------------------+-------------------+
|         2         |         1         |         4         |         1         |
+-------------------+-------------------+-------------------+-------------------+
|packageMark        |packageVersion     |packageType        |packageTypeVersion |
|包标识             |包版本                                 |类型版本           |
+-------------------+-------------------+-------------------+-------------------+

包参数区
+-----------------------------------------------------------+
|                             8                             |
+-----------------------------+-----------------------------+
|              4              |              4              |
+-----------------------------+-----------------------------+
|packageResAmount             |packageOption                |
|资源数量                     |包参数区(位标志待定义)       |
+-----------------------------+-----------------------------+

资源条目区
  一级条目
  动画组信息条目区
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|                                                          128                                                                              |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|         4         |         4         |         4         |         4         |         4         |        107        |         1         |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|resAnIndex         |resAnGroupAmount   |resWidth           |resHeight          |resImageHeaderPos  |resNameStr         |resNameEnd '\0'    |
|动画资源组编号     |动画资源组数量     |资源原始宽度       |资源原始高度       |动画子资源头起始位 |动画资源名字符串   |字符串结尾符       |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+

资源条目区
  二级条目
  动画内的图片信息条目区 -- AnRP
  也可以作为数据区-分段定长 -- AnRPH
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|                                                 32                                                                                                            |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|         4         |         4         |         4         |         4         |         4         |         4         |         4         |         4         |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|resImageIndex      |resImageDataPos    |resSize            |resTitlePy         |resCutLeft         |resCutTop          |resCutWidth        |resCutHeight       |
|动画子资源编号     |资源起始位         |资源大小           |资源标签定位       |资源像素切除量-左  |资源像素切除量-上  |资源像素切除后宽度 |资源像素切除后高度 |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+

'''

''' AnRPD
包标识区
+-------------------------------------------------------------------------------+
|                                       8                                       |
+-------------------+-------------------+-------------------+-------------------+
|         2         |         1         |         4         |         1         |
+-------------------+-------------------+-------------------+-------------------+
|packageMark        |packageVersion     |packageType        |packageTypeVersion |
|包标识             |包版本                                 |类型版本           |
+-------------------+-------------------+-------------------+-------------------+

包参数区
+-----------------------------------------------------------+
|                             8                             |
+-----------------------------+-----------------------------+
|              4              |              4              |
+-----------------------------+-----------------------------+
|packageResAmount             |packageOption                |
|资源数量                     |包参数区(位标志待定义)       |
+-----------------------------+-----------------------------+

数据区
--------------------+-------------------+-------------------+
|      数量由 packageResAmount * resAnGroupAmount 决定      |
+-------------------+-------------------+-------------------+
|       变长        |        变长       |        变长       |
+-------------------+-------------------+-------------------+
|imageData          |imageData          |imageData          |
|裁剪后的图片数据流 |裁剪后的图片数据流 |裁剪后的图片数据流 |
+-------------------+-------------------+-------------------+
'''


import struct, os
import getopt, sys

#将自身所在目录添加到 python 搜索路径
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import atx, anrpDefinitionInfo
import imageProcess
import updateCheck

class anrp:
    def __init__(self, packageName = None, debugMode = False):
        '''
        '''
        self.packageName = packageName
        self.debugMode = debugMode

        # 默认设置和数据定义
        self.packageMark = 'SM'
        self.packageVersion = '1'
        self.packageType = 'AnRP'
        self.packageTypeVersion = '1'

        self.packageResAmount = 0
        self.packageOption = 0

        self.packageAnHeaderList = []
        self.packageImageHeaderList = []
        self.packageImageDatalist = []
        return

    def PrintInfo(self):
        print 'self.packageMark:', self.packageMark
        print 'self.packageVersion:', self.packageVersion
        print 'self.packageType:', self.packageType
        print 'self.packageTypeVersion:', self.packageTypeVersion

        print 'self.packageResAmount:', self.packageResAmount
        print 'self.packageOption:', self.packageOption

        for anHeaderDictX in self.packageAnHeaderList:
            print anHeaderDictX

        for imageHeaderDictX in self.packageImageHeaderList:
            print imageHeaderDictX
        return

    def PrintImageInfo(self):
        imageProcessObj = imageProcess.imageProcess()

        print 'len(self.packageImageHeaderList):', len(self.packageImageHeaderList)
        print 'len(self.packageImageDatalist):', len(self.packageImageDatalist)
        for x in range(len(self.packageImageHeaderList)):
            #计算出图片宽度
            packageImageHeaderX = self.packageImageHeaderList[x]
            width = packageImageHeaderX['resCutedWidth']
            height = packageImageHeaderX['resCutedHeight']
            print width, height, packageImageHeaderX['resSize']

            imageProcessObj.PrintRGB555Data(width, height, self.packageImageDatalist[x])

        return

    def GetDataFromOneAtx(self, atxResName, atxBaseDirStr = None):
        print "anrp.GetDataFromOneAtx('%s', '%s')" % (atxResName, atxBaseDirStr)

        atxObj = atx.atxClass()
        atxObj.GetOneAtxData(atxResName=atxResName, atxBaseDirStr=atxBaseDirStr)

        self.packageResAmount += 1 #资源包内动画组数量 +1
        atxObj.packageAnHeaderList[0]['resAnIndex'] = self.packageResAmount

        self.packageAnHeaderList += atxObj.packageAnHeaderList
        self.packageImageHeaderList += atxObj.packageImageHeaderList
        self.packageImageDatalist += atxObj.packageImageDatalist

        return

    def GetDataFromOneGroupAtx(self, anrpResName, anrpBaseDirStr = None, cacheMode = False):
        '''当 cacheMode == False 时:表示不使用中间文件缓存机制
        缓存默认的存放目录为 output'''
        print "anrp.GetDataFromOneGroupAtx('%s', '%s')" % (anrpResName, anrpBaseDirStr)
        anrpDefObj = anrpDefinitionInfo.anrpDefinitionInfoClass(anrpResName)
        anrpDefObj.LoadXml(anrpBaseDirStr=anrpBaseDirStr)

        if cacheMode:
            print 'cacheMode'
            for resSourceX in anrpDefObj.resSourceList:
                atxPackageName = resSourceX['resName']
                atxResBaseDir = resSourceX['resPath']
                if anrpBaseDirStr != None:
                    atxFileDir = os.path.join(anrpBaseDirStr, 'output')
                else:
                    atxFileDir = 'output'
                atxRpdFileFullPath = os.path.join(atxResBaseDir, '%s.xml' % atxPackageName)

                #检查这个 ATX 是否已经有生成中间文件 AnRP 文件
                isNeedUpdate = updateCheck.IsNeedUpdate4AtxXml(atxPackageName, atxResBaseDir, atxFileDir)

                if isNeedUpdate:
                    #如果没有生成，或者需要更新就再次生成
                    anrpObj = anrp(packageName=atxPackageName, debugMode=False)
                    anrpObj.GetDataFromOneAtx(atxResName=atxPackageName, atxBaseDirStr=atxResBaseDir)
                    anrpObj.Save(outputDirStr=atxFileDir)
                    del anrpObj #显式删除对象以释放内存
                else:
                    print '%s is up to date' % atxRpdFileFullPath

                #如果已经生成就直接读取
                self.GetDataFromOneAnRPFile(
                    packageName=atxPackageName,
                    inputDirStr=atxFileDir,
                    cover=False
                )
        else:
            for resSourceX in anrpDefObj.resSourceList:
                self.GetDataFromOneAtx(resSourceX['resName'], resSourceX['resPath'])

        return

    def Save(self, packageName = None, outputDirStr = None):
        if self.debugMode:
            self.PrintImageInfo()
        if packageName == None:
            packageName = self.packageName
        packageName = u'%s.anrp' % packageName
        if outputDirStr != None:
            packageName = os.path.join(outputDirStr, packageName)

        print "anrp.Save('%s')" % packageName

        try:
            f = open(packageName, 'wb')
        except:
            print "Error! open('%s', 'wb')" % packageName
            raise

        # 写文件头信息
        # 写包标识区
        f.write(self.packageMark)
        f.write(self.packageVersion)
        f.write(self.packageType)
        f.write(self.packageTypeVersion)

        # 写包参数区
        f.write(struct.pack('I', self.packageResAmount))
        f.write(struct.pack('I', self.packageOption))

        # 写动画组信息条目区
        # 一级条目
        resImageHeaderPos = 16 + len(self.packageAnHeaderList) * 128 #16 为 groud 包头标志长度, 128 为每条一级条目的长度
        for anHeaderDictX in self.packageAnHeaderList:
            f.write(struct.pack('I', anHeaderDictX['resAnIndex']))
            f.write(struct.pack('I', anHeaderDictX['resAnGroupAmount']))
            f.write(struct.pack('I', anHeaderDictX['resWidth']))
            f.write(struct.pack('I', anHeaderDictX['resHeight']))
            f.write(struct.pack('I', resImageHeaderPos))
            #f.write(self._ExpandStr(anHeaderDictX['resName']))
            f.write(struct.pack('108s', self._ExpandStr(anHeaderDictX['resName'])))

            resImageHeaderPos += anHeaderDictX['resAnGroupAmount'] * 32 # 32为二级条目每条的长度

        # 写入动画图片信息条目区
        # 二级条目
        resImageDataPos = resImageHeaderPos
        for imageHeaderDictX in self.packageImageHeaderList:
            f.write(struct.pack('I', imageHeaderDictX['resImageIndex']))
            f.write(struct.pack('I', resImageDataPos))
            f.write(struct.pack('I', imageHeaderDictX['resSize']))
            f.write(struct.pack('I', imageHeaderDictX['resTitlePy']))
            f.write(struct.pack('I', imageHeaderDictX['resCutedLeft']))
            f.write(struct.pack('I', imageHeaderDictX['resCutedTop']))
            f.write(struct.pack('I', imageHeaderDictX['resCutedWidth']))
            f.write(struct.pack('I', imageHeaderDictX['resCutedHeight']))

            resImageDataPos += imageHeaderDictX['resSize']

        # 写资源数据区
        #f.write('------------------for test------------------')
        #for imageDataX in self.packageImageDatalist:
        for x in range(len(self.packageImageDatalist)):
            imageDataX = self.packageImageDatalist[x]
##            #----测试输出
##            if x <= 100:
##                tf = open('%d.rgb555' % x, 'wb')
##                for dataX in imageDataX:
##                    tf.write(struct.pack('B', dataX))
##                tf.close()
##            #----测试输出结束
            #print '.',
            #f.write(imageDataX)
            #输出到文件
            for dataX in imageDataX:
                f.write(struct.pack('B', dataX))

        f.close()
        return


    def _ExpandStr(self, line):
        '''在字符串后添加'\0'(兼容 C 语言)，最后将字符串扩充到 107+1 个字节'''
        if len(line) > 107:
            raise Exception(u'文件名长度超过限制')
        diff = 107 - len(line)
        line += chr(0) * (diff+1) #使用 '\0' 填空，并且最后添加一个作为兼容 C 的字符串结束符
        return line

    def _SplitStrSpace(self, line):
        '''截断字符串后面多余的 \0'''
        line = line.rstrip(chr(0))
        return line

    def Load(self, packageName = None, inputDirStr = None):
        return self.GetDataFromOneAnRPFile(packageName = None, inputDirStr = None, cover = True)

    def LoadAppend(self, packageName = None, inputDirStr = None):
        return self.GetDataFromOneAnRPFile(packageName = None, inputDirStr = None, cover = False)

    def GetDataFromOneAnRPFile(self, packageName = None, inputDirStr = None, cover = True):
        '''当 cover == True 时装载动作会覆盖内存中已有的数据，其他情况下是追加数据'''
        if packageName == None:
            packageName = self.packageName
        packageName = u'%s.anrp' % packageName
        if inputDirStr != None:
            packageName = os.path.join(inputDirStr, packageName)

        try:
            f = open(packageName, 'rb')
        except:
            print "Error! open('%s', 'rb')" % packageName
            raise

        # 读文件头信息
        # 读包标识区
        self.packageMark = f.read(2)
        self.packageVersion = f.read(1)
        self.packageType = f.read(4)
        self.packageTypeVersion = f.read(1)

        # 读包参数区
        packageResAmount = struct.unpack('I', f.read(4))[0]
        self.packageOption = struct.unpack('I', f.read(4))[0]
        if cover:
            self.packageResAmount = packageResAmount
        else:
            self.packageResAmount += packageResAmount

        # 读动画组信息条目区
        # 一级条目
        packageAnHeaderList = []
        for x in range(packageResAmount):
            anHeaderDict = {}
            anHeaderDict['resAnIndex'] = struct.unpack('I', f.read(4))[0]
            anHeaderDict['resAnGroupAmount'] = struct.unpack('I', f.read(4))[0]
            anHeaderDict['resWidth'] = struct.unpack('I', f.read(4))[0]
            anHeaderDict['resHeight'] = struct.unpack('I', f.read(4))[0]
            anHeaderDict['resImageHeaderPos'] = struct.unpack('I', f.read(4))[0]
            anHeaderDict['resName'] = self._SplitStrSpace(f.read(108))

            packageAnHeaderList.append(anHeaderDict)
        if cover:
            self.packageAnHeaderList = packageAnHeaderList
        else:
            self.packageAnHeaderList += packageAnHeaderList

        # 读入动画图片信息条目区
        # 二级条目
        packageImageHeaderList = []
        for x in range(packageResAmount):
            for y in range(packageAnHeaderList[x]['resAnGroupAmount']):
                imageHeaderDict = {}
                imageHeaderDict['resImageIndex'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resImageDataPos'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resSize'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resTitlePy'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resCutedLeft'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resCutedTop'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resCutedWidth'] = struct.unpack('I', f.read(4))[0]
                imageHeaderDict['resCutedHeight'] = struct.unpack('I', f.read(4))[0]

                packageImageHeaderList.append(imageHeaderDict)
        if cover:
            self.packageImageHeaderList = packageImageHeaderList
        else:
            self.packageImageHeaderList += packageImageHeaderList

        # 读入图片数据
        packageImageDatalist = []
        x = 0
        for imageHeaderDictX in packageImageHeaderList:
            packFormatStr = '%dB' % imageHeaderDictX['resSize']
            packBufferStr = f.read(imageHeaderDictX['resSize'])
            packageImageDatalist.append(struct.unpack(packFormatStr, packBufferStr))
        if cover:
            self.packageImageDatalist = packageImageDatalist
        else:
            self.packageImageDatalist += packageImageDatalist

        if self.debugMode:
            self.PrintImageInfo()
        return
    
    def GetPNGFromAnRPFile(self,packageName = None):
        if packageName == None:
            packageName = self.packageName
        lenth = len(self.packageImageDatalist)
        for i in range(lenth):
            imageDataX = self.packageImageDatalist[i]
            imageHeaderDictX = self.packageImageHeaderList[i]
            width = imageHeaderDictX['resCutedWidth']
            height = imageHeaderDictX['resCutedHeight']
            rgb555Data = imageDataX
            rgb555Data = []
            f = open('%s.anrp' % packageName, 'rb')
            f.seek(imageHeaderDictX['resImageDataPos'])

            packFormatStr = '%dB' % imageHeaderDictX['resSize']
            packBufferStr = f.read(imageHeaderDictX['resSize'])
            rgb555Data = struct.unpack(packFormatStr, packBufferStr)
            imageProcessObj = imageProcess.imageProcess()
            rgb888DataList = imageProcessObj.GetRGB888from555(width, height, rgb555Data)
            imageObj = imageProcessObj.CreateFromRGB888(width, height, rgb888DataList)
            imageProcessObj.Save2PNG(imageObj, '%s_%s' %(packageName,i))
        #del anrpObj
        return
def test():
    packageName = 'ghhl001'
    debugMode = False
    anrpObj = anrp(packageName, debugMode)
    atxResName = 'ghhl001'
    resBaseDir = 'C:\\Users\\ZLove\\Desktop\\anrp12'
    anrpResName = None
    if atxResName != None:
        anrpObj.GetDataFromOneAtx(atxResName=atxResName, atxBaseDirStr=resBaseDir)
        anrpObj.Save()
    elif anrpResName != None:
        anrpObj.GetDataFromOneGroupAtx(anrpResName, anrpBaseDirStr=resBaseDir, cacheMode=cacheMode)
    else:
        print 'atxResName == None and anrpResName == None'

def usage():
    print u'usage: anrp {-c [-r]| -l | -u} [--debug] -n packageName {--atxResName atxResName | --anrpResName anrpResName [--cacheMode]} [--resBaseDir resBaseDir --outputDir outputDir]'
    print u'选项说明：'
    print u'    -h help, 显示本帮助信息'
    print u'    -c create, 打包 ATX 资源到 AnRP 包文件'
    print u'    -l list, 列表显示 AnRP 包文件中的内容清单'
    print u'    -u upack, 解析 AnRP 包文件为PNG图片'
    print u'    --debug, debug 开启模式'
    print u'    -r rebuild, 强制重新生成目标文件'
    print u'    -n packageName, AnRP 包文件名'
    print u'    --atxResName atxResName, ATX 资源名'
    print u'    --anrpResName anrpResName, AnRP 资源名'
    print u'    --cacheMode, 缓存模式, --anrpResName 开关下有效'
    print u'    --resBaseDir resBaseDir, ATX/AnRP 资源所在路径'
    print u'    --outputDir outputDir, AnRP 包文件输出路径，默认为当前目录'
    return

def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hclurn:",
            ["help", "create", "list", "upack","rebuild", "debugMode", "packageName=", "atxResName=", "anrpResName=", "cacheMode", "resBaseDir=", "outputDir="]
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    #初始化状态值
    workMode = None
    rebuild = False
    packageName = None

    debugMode = False

    atxResName = None
    anrpResName = None

    cacheMode = False

    resBaseDir = None
    outputDir = None
    #处理命令行信息
    for opt, optarg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--create"):
            workMode = 'create'
        elif opt in ("-l", "--list"):
            workMode = 'list'
        elif opt in ("-u", "--upack"):
            workMode = 'upack'
        elif opt in ("-r", "--rebuild"):
            rebuild = True
        elif opt in ("--debugMode",):
            debugMode = True
        elif opt in ("-n", "--packageName"):
            packageName = optarg
        elif opt in ("--atxResName",):
            atxResName = optarg
        elif opt in ("--anrpResName",):
            anrpResName = optarg
        elif opt in ("--cacheMode",):
            cacheMode = True
        elif opt in ("--resBaseDir",):
            resBaseDir = optarg
        elif opt in ("--outputDir",):
            outputDir = optarg
        else:
            assert False, "unhandled option"

    #执行
    if packageName == None:
        print 'packageName == None'
        usage()
        raise

    if workMode == 'create':
        anrpObj = anrp(packageName, debugMode)
        if atxResName != None:
            anrpObj.GetDataFromOneAtx(atxResName=atxResName, atxBaseDirStr=resBaseDir)
        elif anrpResName != None:
            anrpObj.GetDataFromOneGroupAtx(anrpResName, anrpBaseDirStr=resBaseDir, cacheMode=cacheMode)
        else:
            print 'atxResName == None and anrpResName == None'
            usage()
            raise

        anrpObj.Save(outputDirStr=outputDir)
        return
    elif workMode == 'list':
        anrpObj = anrp(packageName)
        inputDirStr = None
        anrpObj.Load()
        #anrpObj.Load(inputDirStr=inputDirStr)
        anrpObj.PrintInfo()
        return
    elif workMode == 'upack':
        anrpObj = anrp(packageName)
        inputDirStr = None
        anrpObj.Load()
        anrpObj.GetPNGFromAnRPFile()
        return



if __name__ == "__main__":
    import time
    startTime = time.time()
    #main()
    test()
    print 'TIME:', time.time() - startTime
