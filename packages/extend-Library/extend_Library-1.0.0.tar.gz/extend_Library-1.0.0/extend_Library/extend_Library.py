#-*-coding=utf-8-*-

from PIL import Image
from appium import webdriver
from AppiumLibrary.utils import ApplicationCache
from AppiumLibrary.locators import ElementFinder
from AppiumLibrary.keywords import keywordgroup
from datetime import datetime
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

import os
import sys
import tempfile  
''' 
如何你的应用程序需要一个临时文件来存储数据，但不需要同其他程序共享，那么用TemporaryFile函数创建临时文件是最好的选择。其他的应用程序是无法找到或打开这个文件的，因为它并没有引用文件系统表。用这个函数创建的临时文件，关闭后会自动删除
'''
import shutil
'''
是一种高层次的文件操作工具
'''


PATH = lambda p: os.path.abspath(p)
#返回path规范化的绝对路径
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class extend_Library(object):

    def __init__(self):
        self.key = 'ENCODE_AES_KEY16'
        self.iv  = 'This is an IV456'
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS) 
        self.unpad = lambda s : s[0:-ord(s[-1])]
        self._cache = ApplicationCache()
        self.driver = self._cache.current
        

    def encrypt(self, text):
        text = self.pad(text)
        self.obj1 = AES.new(self.key, self.mode, self.iv)        
        self.ciphertext = self.obj1.encrypt(text)
        return b2a_hex(self.ciphertext)
     
    
    def decrypt(self, db_password):
        aaa = db_password[0:32]
        bbb = db_password[32:64]
        self.obj2 = AES.new(self.key, self.mode,a2b_hex(aaa))
        plain_text  = self.obj2.decrypt(a2b_hex(bbb))
        return self.unpad(plain_text.rstrip('\0'))
       

    def get_screenshot_by_element(self, locator):
        """通过获取元素的height和width来截取整个元素的图片,输入参数为元素的locator

        | locator          | 
       
        Examples:
         element = self.driver.find_element_by_id("com.android.deskclock:id/imageview")
         |get_screenshot_by_element(element)|
         
        """      
        element = self._element_find(locator, True, True)      
        #先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        #获取元素bounds(左上角和右下角)
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        #截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        '''自定义截取范围
         输入参数为要截取图片的起始和结束坐标（start_x, start_y, end_x, end_y），保存在了临时目录下
         临时目录路径为：TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
        '''
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def write_to_file( self, dirPath, imageName, form = "png"):
        '''将截屏文件复制到指定目录下
            将保存在临时目录的图片复制到指定路径下
            参数说明：
            dirPath：指定复制到的目录
            imageName:保存的图片名称
            form:保存的图片格式，默认为"png"格式
        '''
        if not os.path.isdir(dirPath):
            #os.path.isfile() 和os.path.isdir()函数分别检验给出的路径是一个文件还是目录
            os.makedirs(dirPath)
            #os.makedirs(path) 递归的创建目录
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))
        #shutil.copyfile( src, dst) 从源src复制到dst中去,如果当前的dst已存在的话就会被覆盖掉

    def load_image(self, image_path):
        '''加载目标图片供对比用
                    参数：image_path ：目标图片路径
                    返回值：已经打开的图片
        '''
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)

    #http://testerhome.com/topics/202
    def same_as(self, image_path, percent):
        '''与临时目录图片进行相似比对
            参数：image_path:与临时路径做比较的图片路径
            percent:设置相似度，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        '''
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = self.load_image(image_path)

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        '''
        differ算法:histograme1数组各元素减去histogram2数组各元素，差求平方后相加，和除以histogream1元素个数，最后算根方差，值越大的图片相似度越低，值越小相似度越高，若为0则100%相似
        '''
        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, \
                                                         histogram1, histogram2)))/len(histogram1))
        if differ <= percent:
            return True
        else:
            return False

    def compare_str(self,str1,str2):

        '''
        u判断"str1"是否包含在字符串"str2"中，如果包含返回1，不包含返回0
        | str1                   | str2                 | 
        ''' 
        if str1 in str2:
            return 1
        else:
            return 0

    def del_string_space(self,string):   

        '''去除字符串中的回车
        ''' 
        string = string.replace('\n','')
        return string 



