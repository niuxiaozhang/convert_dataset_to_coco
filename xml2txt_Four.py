#coding:utf-8
import xml.etree.ElementTree as ET
import glob
import os
import random
trainfile = open('G:\Dataset\min40x40/train.txt','a')
def get_classes_and_index(path):
    D = {}
    f = open(path)
    for line in f:
        temp = line.rstrip().split(',', 2)
        print("temp[0]:" + temp[0] + "\n")
        print("temp[1]:" + temp[1] + "\n")
        D[temp[1].replace(' ', '')] = temp[0]
    return D

for name2 in glob.glob(r'G:\Dataset\min40x40\train\XML/*.xml'):
    print(name2)
    in_file = open(name2,encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    filename=root.findtext('filename')
    print(str(filename))
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text.replace(' ', '')
        # 如果该类物体不在我们的yolo训练列表中，跳过
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        trainfile.write(str(filename) + "," + xmin + ','+ ymin + ',' + xmax+ ',' + ymax + ',' + cls + '\n')

trainfile.close()

