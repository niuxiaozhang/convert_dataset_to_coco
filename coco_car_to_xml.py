# coding=utf-8

import xml.dom
import xml.dom.minidom
import os
import cv2
import json

_IMAGE_PATH= r'D:\ThunderDownload\coco\images'
_INDENT = '' * 4
_NEW_LINE = '\n'
_FOLDER_NODE = 'train2017'
_ROOT_NODE = 'annotation'
_DATABASE_NAME = 'COCO'
_ANNOTATION = 'train2017'
_DIFFICULT = '0'
_TRUNCATED = '0'
_POSE = 'Unspecified'
# 保存的目录
_ANNOTATION_SAVE_PATH = r'G:\Dataset\car_dataset\coco'


# 创建节点
def createElementNode(doc, tag, attr):  # 创建一个元素节点
    element_node = doc.createElement(tag)
    # 创建一个文本节
    text_node = doc.createTextNode(attr)
    # 将文本节点作为元素节点的子节
    element_node.appendChild(text_node)
    return element_node


# 创建子节点
def createChildNode(doc, tag, attr, parent_node):
    child_node = createElementNode(doc, tag, attr)
    parent_node.appendChild(child_node)


# 创建 object 节点以及子节点
def createObjectNode(doc, attrs):
    object_node = doc.createElement('object')
    createChildNode(doc, 'name', attrs['name'], object_node)
    createChildNode(doc, 'pose', _POSE, object_node)
    createChildNode(doc, 'truncated', _TRUNCATED, object_node)
    createChildNode(doc, 'difficult', _DIFFICULT, object_node)
    bndbox_node = doc.createElement('bndbox')
    createChildNode(doc, 'xmin', str(int(attrs['bndbox'][0])), bndbox_node)
    createChildNode(doc, 'ymin', str(int(attrs['bndbox'][1])), bndbox_node)
    createChildNode(doc, 'xmax', str(int(attrs['bndbox'][0] + attrs['bndbox'][2])), bndbox_node)
    createChildNode(doc, 'ymax', str(int(attrs['bndbox'][1] + attrs['bndbox'][3])), bndbox_node)
    object_node.appendChild(bndbox_node)
    return object_node


# 写入 xml 文件
def writeXMLFile(doc, filename):
    tmpfile = open('tmp.xml', 'w')
    doc.writexml(tmpfile, addindent='' * 4, newl='\n', encoding='utf-8')
    tmpfile.close()
    # 删除第一行默认添加的标记
    fin = open('tmp.xml')
    fout = open(filename, 'w')
    lines = fin.readlines()
    for line in lines[1:]:
        if line.split():
            fout.writelines(line)
    fin.close()
    fout.close()

def create_root_node(saveName, width, height, channel):
    my_dom = xml.dom.getDOMImplementation()
    doc = my_dom.createDocument(None, _ROOT_NODE, None)

    # root node
    root_node = doc.documentElement

    # folder node
    createChildNode(doc, 'folder', _FOLDER_NODE, root_node)

    # filename node
    createChildNode(doc, 'filename', saveName + '.jpg', root_node)

    # source node
    source_node = doc.createElement('source')
    # source child node
    createChildNode(doc, 'database', _DATABASE_NAME, source_node)
    root_node.appendChild(source_node)

    # size node
    size_node = doc.createElement('size')
    createChildNode(doc, 'width', str(width), size_node)
    createChildNode(doc, 'height', str(height), size_node)
    createChildNode(doc, 'depth', str(channel), size_node)
    root_node.appendChild(size_node)

    return doc, root_node


def main():
    img_path = r'D:\ThunderDownload\coco\images\train2017'
    fileList = os.listdir(img_path)
    if fileList == 0:
        os._exit(-1)

    with open('coco_train.json', 'r') as f:
        ann_data = json.load(f)

    current_dirpath = os.path.dirname(os.path.abspath('__file__'))

    if not os.path.exists(_ANNOTATION_SAVE_PATH):
        os.mkdir(_ANNOTATION_SAVE_PATH)

    for imageName in fileList:
        saveName = imageName.strip('.jpg')
        img = cv2.imread(os.path.join(img_path, imageName))
        height, width, channel = img.shape

        doc, root_node = create_root_node(saveName, width, height, channel)
        is_save = False
        for ann in ann_data:
            imgName = str(ann['filename'])
            for j in range(12 - len(imgName)):
                imgName = '0' + imgName
            if saveName == imgName:
                print("ann['name']", ann['name'])
                if ann['name'] == 'car' or ann['name'] == 'bus' or ann['name'] == 'truck':
                    is_save = True
                    object_node = createObjectNode(doc, ann)
                    root_node.appendChild(object_node)
        if is_save:
            # 写入文件
            xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.xml'))
            # 构建XML文件名称
            print(xml_file_name)
            writeXMLFile(doc, xml_file_name)
            img_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.jpg'))
            cv2.imwrite(img_file_name, img)




if __name__ == "__main__":
    main()
