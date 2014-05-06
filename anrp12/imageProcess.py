#! /usr/bin/env python
#coding=utf-8


import struct
from PIL import Image


'''PIL 的 图片坐标是从 0 开始计数的
'''


PICTRUE_ORIG_WIDTH = 160

class imageProcess:
    '''AnRP 相关的图片处理'''
    def __init__(self, imageFilename = None):
        self.imageFilename = imageFilename
        self.imageObj = None
        self.isBlackImage = False #标明是否是整张黑图片

        return

    def OpenPNG(self, pngFilename = None):
        if pngFilename == None:
            return False
        else:
            self.imageFilename = pngFilename

        #装载图片信息到内存
        self.imageObj = Image.open(pngFilename)
        if self.imageObj == None:
            return False

        return True

    def PrintImage(self, imageObj = None):
        if imageObj == None:
            imageObj = self.imageObj
        print imageObj.format, imageObj.mode, imageObj.size, imageObj.palette, imageObj.info

        imageWidth = imageObj.size[0]
        imageHeight = imageObj.size[1]
        for y in range(imageHeight):
            for x in range(imageWidth):
                pixel = imageObj.getpixel((x, y))
                if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                    print '.',
                else:
                    print 0,
            print ' '

    def GetBorderTop(self, imageObj = None):
        if imageObj != None:
            self.imageObj = imageObj

        imageWidth = self.imageObj.size[0]
        imageHeight = self.imageObj.size[1]
        for y in range(imageHeight):
            for x in range(imageWidth):
                #print x,y
                pixel = self.imageObj.getpixel((x, y))
                if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
                    return y

    def GetBorderBottom(self, imageObj = None):
        if imageObj != None:
            self.imageObj = imageObj

        imageWidth = self.imageObj.size[0]
        imageHeight = self.imageObj.size[1]
        for y in reversed(range(imageHeight)):
            for x in reversed(range(imageWidth)):
                #print x,y
                pixel = self.imageObj.getpixel((x, y))
                if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
                    return y

    def GetBorderLeft(self, imageObj = None):
        if imageObj != None:
            self.imageObj = imageObj

        imageWidth = self.imageObj.size[0]
        imageHeight = self.imageObj.size[1]
        for x in range(imageWidth):
            for y in range(imageHeight):
                #print x,y
                pixel = self.imageObj.getpixel((x, y))
                if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
                    return x

        #第一个检查的是左边界，所以只在这里做判断
        #print x,y,imageHeight,imageWidth
        if x == imageWidth-1 and y == imageHeight-1:
            #发现是空白黑图片
            return

    def GetBorderRight(self, imageObj = None):
        if imageObj != None:
            self.imageObj = imageObj

        imageWidth = self.imageObj.size[0]
        imageHeight = self.imageObj.size[1]
        for x in reversed(range(imageWidth)):
            for y in reversed(range(imageHeight)):
                #print x,y
                pixel = self.imageObj.getpixel((x, y))
                if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
                    return x

    def CutBlackBorder(self, imageObj = None):
        '''切除图片四周的黑边部分
        PIL 似乎有 Bug 会多在右边界切像素'''
        
        if imageObj != None:
            self.imageObj = imageObj
        #self.PrintImage(self.imageObj)
        
        self.cutLeft = self.GetBorderLeft()
        if self.cutLeft == None:
            #如果图片是整张黑色
            print "asff"
            self.isBlackImage = True
            self.cutLeft = 78
            self.cutTop = 80
            self.cutRight = 82
            self.cutBottom = 81
        else:
            self.cutTop = self.GetBorderTop()
            self.cutRight = self.GetBorderRight() + 1
            self.cutBottom = self.GetBorderBottom() + 1

        #调整切割点，保证切割出来的图像像素宽度为 4 的整倍数
        width = self.cutRight - self.cutLeft
        remainder = width % 4
        #print self.cutLeft, self.cutRight
        #print 'width:', width
        #print 'remainder:', remainder
        if remainder != 0:
            #宽度不是 4 的整倍数
            pixel = 4 - remainder #需要填补的像素量
            if (PICTRUE_ORIG_WIDTH - self.cutRight) > pixel:
                #优先扩宽图像右边
                self.cutRight += pixel
            else:
                self.cutLeft -= pixel

        cropBox = (self.cutLeft, self.cutTop, self.cutRight, self.cutBottom)
        #print cropBox

        self.imageObj = self.imageObj.crop(cropBox)
        #self.PrintImage(self.imageObj)
        return self.imageObj

    def GetRGBData(self, colorName = None, imageObj = None):
        if imageObj == None:
            imageObj = self.imageObj
        if colorName == None or colorName == 'all':
            #默认返回所有数据
            return imageObj.getdata()

        if colorName == 'red':
            colorIndex = 0
        elif colorName == 'green':
            colorIndex = 1
        elif colorName == 'blue':
            colorIndex = 2

        return imageObj.getdata(colorIndex)

    def GetRGB555Data(self, imageObj = None):
        if imageObj != None:
            self.imageObj = imageObj

        imageData = self.imageObj.getdata()
        rgb555Data = []

        for bandX in imageData:
            r = int(bandX[0]) & 0xF8
            g = int(bandX[1]) & 0xF8
            b = int(bandX[2]) & 0xF8

            RGB555Data = r << 7
            RGB555Data += g << 2
            RGB555Data += b >> 3

            a = RGB555Data & 0xFF
            b = (RGB555Data >> 8)& 0xFF
            rgb555Data.append(a)
            rgb555Data.append(b)

        return rgb555Data

    def GetRGB888from555(self, width, height, rgb555DateList):
        '''
        RGB555的格式(二进制):
        byte1: XBBB BBGG
        byte2: GGGR RRRR
        RGB888格式
        byte1: BBBB B000
        byte2: GGGG G000
        byte3: RRRR R000
        '''
        rgb888DataList = []
        pixCount = width * height
        i = 0
        while(i != pixCount*2):
            rgb555Data = 0
            rgb555Data = rgb555DateList[i+1];
            rgb555Data = rgb555Data << 8;
            rgb555Data = rgb555Data + rgb555DateList[i];
            #RGB555
            #算法 A。这个算法实质上与 B 是一样的
            r = ((rgb555Data >> 7) & 0xF8);
            g = ((rgb555Data >> 2) & 0xF8);
            b = ((rgb555Data << 3) & 0xF8);

            rgb888DataList.append(b)
            rgb888DataList.append(g)
            rgb888DataList.append(r)

            if rgb555Data != 0:
                pass

            i += 2

        return rgb888DataList

    def CreateFromRGB888(self, width, height, rgb888Data):
        imageObj = Image.new('RGB', (width,height), (0,0,0))

        pos = 0
        for y in range(height):
            for x in range(width):
                imageObj.putpixel((x, y), rgb888Data[pos]*65536 + rgb888Data[pos+1]*256 + rgb888Data[pos+2])
                pos += 3

        return imageObj

    def Save2PNG(self, imageObj, filename):
        imageObj.save('%s.png' % filename)
        return

    def PrintRGB555Data(self, width, height, rgb555Data):
        pos = 0
        for y in range(height):
            for x in range(width):
                if rgb555Data[pos] == 0 and rgb555Data[pos+1] == 0:
                    print '.',
                else:
                    print 'O',
                pos += 2
            print ' '

        return

    def PrintRGB888Data(self, width, height, rgb888Data):
        pos = 0
        for y in range(height):
            for x in range(width):
                if rgb888Data[pos] == 0 and rgb888Data[pos+1] == 0 and rgb888Data[pos+2] == 0:
                    print '.',
                else:
                    print 'O',
                pos += 3
            print ' '

        return


if '__main__' == __name__:
    import time
    startime = time.time()
    imageProcessObj = imageProcess()


    imageProcessObj.OpenPNG("11.png")
    imageObj = imageProcessObj.CutBlackBorder()
    imageObj.save('output.png', 'PNG')
    print 'TotalL:',time.time()-startime
 
