#!/usr/bin/env python
# --coding:utf-8--
#批量转换瓦片存储规格，支持google到amap(type=0)，arcgis(使用水经注下载的google影像，z需要减1)到amap(type=1)，兼容wndows和linux
#test_data_for_transform为测试数据

import os
import shutil



def trim_zero(input):
    for i in range(len(input)):
        if input[i]=="0":
            continue
        else:
            return input[i:]

def parse(input, transType, result_z_x_y):
    if 0 == transType:      #google到amap
        z = str(int(trim_zero(input.split(os.path.sep)[-3])))
        y = trim_zero(input.split(os.path.sep)[-1]).split(".")[0]
        x = trim_zero(input.split(os.path.sep)[-2])
        print z, x , y
        result_z_x_y.append( (z, x, y) )
    elif 1 == transType:      #arcgis到amap
        z = str ( int( trim_zero(input.split(os.path.sep)[-3][1:]) )-1 )
        x = trim_zero(input.split(os.path.sep)[-1][1:]).split(".")[0]
        y = trim_zero(input.split(os.path.sep)[-2][1:])
        print z, x , y
        result_z_x_y.append( (z, x, y) )


def fill_zero_z(input):
    length = len(input)
    zero_num = 2-length
    result = ""
    for i in range(zero_num):
        result += "0"
    return result+input

def fill_zero_x_y(input):
    length = len(input)
    zero_num = 6-length
    result = ""
    for i in range(zero_num):
        result += "0"
    return result+input

def arcgis_zxy2path(input, basepath):
    z = input[0]
    x = input[1]
    y = input[2]
    return basepath + os.path.sep + "L" + fill_zero_z( str(int(z)+1) ) + os.path.sep + "R" + fill_zero_x_y(y) + os.path.sep + "C" + fill_zero_x_y(x) + ".png"


def arcgis2mapabc(input, old_basepath, new_basepath):
    old_path = arcgis_zxy2path(input, old_basepath)
    z = input[0]
    x = input[1]
    y = input[2]
    new_path_dir = new_basepath + os.path.sep + z + os.path.sep + str(int(x)/10) + os.path.sep + str(int(y)/10)
    if not os.path.exists(new_path_dir):
        os.makedirs(new_path_dir)
    new_path = new_path_dir + os.path.sep + x + "_" + y +".png"
    shutil.copyfile(old_path,  new_path)

def google2mapabc(input, old_basepath, new_basepath):
    z = input[0]
    x = input[1]
    y = input[2]
    old_path = old_basepath + os.path.sep + z + os.path.sep + x + os.path.sep + y + ".png"
    new_path_dir = new_basepath + os.path.sep + z + os.path.sep + str(int(x)/10) + os.path.sep + str(int(y)/10)
    if not os.path.exists(new_path_dir):
        os.makedirs(new_path_dir)
    new_path = new_path_dir + os.path.sep + x + "_" + y +".png"
    shutil.copyfile(old_path,  new_path)


if __name__ == "__main__":
    path='c:\\66\\arcgis'
    # path='/data/hainan/input'

    new_path='c:\\66_new'
    # new_path='/data/hainan/output'
    transType = 1
    result_z_x_y = []

    #从原始输入路径中抽取z,x,y
    for dirpath,dirnames,filenames in os.walk(path):
        for file in filenames:
                fullpath=os.path.join(dirpath,file)
                # print fullpath
                parse(fullpath, transType, result_z_x_y)

    if 0 == transType:
        for zxy in result_z_x_y:
            google2mapabc(zxy, path, new_path)
    elif 1 == transType:
        for zxy in result_z_x_y:
            arcgis2mapabc(zxy, path, new_path)
