#! /usr/bin/env python
# coding=utf-8

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
import re
from PIL import Image
import xml.etree.ElementTree as ET
from xml.etree import ElementTree  # 导入ElementTree模块

return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0",
                               "pred_lbbox/concat_2:0"]
pb_file = "./yolov3_bee.pb"
dirpath = './VOC2007/JPEGImages/'
xmlpath = './VOC2007/Annotations/'

def isimage(fn):
    return os.path.splitext(fn)[-1] in (
        '.jpg', '.JPG', '.png', '.PNG')

def main():
    imagelist = []
    for r, ds, fs in os.walk(dirpath):
        for fn in fs:
            if not isimage(fn):
                continue
            fname = os.path.join(r, fn)
            name = os.path.splitext(fname)[0][21:32]
            print(name +'.jpg')


            image_path = fname
            num_classes = 1
            input_size = 608
            graph = tf.Graph()

            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            original_image_size = original_image.shape[:2]
            image_data = utils.image_preporcess(np.copy(original_image), [input_size, input_size])
            image_data = image_data[np.newaxis, ...]

            return_tensors = utils.read_pb_return_tensors(graph, pb_file, return_elements)

            with tf.Session(graph=graph) as sess:
                pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
                    [return_tensors[1], return_tensors[2], return_tensors[3]],
                    feed_dict={return_tensors[0]: image_data})
            # print(pred_sbbox.shape)

            pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                                        np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                                        np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)

            bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, input_size, 0.3)
            # bndbox = np.round(bboxes)
            # bndbox = bboxes
            # print(bndbox[0:4])
            bboxes = utils.nms(bboxes, 0.45, method='nms')
            n = len(bboxes)
            i = 0
            l = []
            for i in range(n):

                bndbox = np.round(bboxes[i])
                # bndbox = int(bnd[:,:4])
                #print(int(bndbox[0]), int(bndbox[1]), int(bndbox[2]), int(bndbox[3]))
                xi = int(bndbox[0])
                yi = int(bndbox[1])
                xa = int(bndbox[2])
                ya = int(bndbox[3])
                z = [xi,yi,xa,ya]
                l.append(z)
                print(l)
                m = l[i][0]
                o = l[i][1]
                q = l[i][2]
                v = l[i][3]
                filename = image_path
                img = Image.open(filename)
                imgname = name + '.jpg'
                imgSize = img.size  # 图片的长和宽
                maxSize = max(imgSize)  # 图片的长边
                minSize = min(imgSize)  # 图片的短边
                # 设置为自己Annotations保存路径
                ########################## 创建xml文件 ################################

                a = ET.Element("annotation")  # 创建根节点
                b = ET.SubElement(a, "folder")  # 创建子节点，并添加数据
                b.text = "bees"
                c = ET.SubElement(a, "filename")  # 创建子节点，并添加数据
                c.text = imgname
                d = ET.SubElement(a, "path")  # 创建子节点，并添加数据
                d.text = fname
                e = ET.SubElement(a, "source")  # 创建子节点，并添加数据
                e1 = ET.SubElement(e, "database")
                e1.text = "Unknown"
                f = ET.SubElement(a, "size")  # 创建子节点，并添加数据
                f1 = ET.SubElement(f, "width")
                f1.text = str(maxSize)
                f2 = ET.SubElement(f, "height")
                f2.text = str(minSize)
                f3 = ET.SubElement(f, "depth")
                f3.text = "3"
                g = ET.SubElement(a, "segmented")  # 创建子节点，并添加数据
                g.text = "0"
                if i ==0:
                    h = ET.SubElement(a, "object")  # 创建子节点，并添加数据
                    h1 = ET.SubElement(h, "name")
                    h1.text = "bee"
                    h2 = ET.SubElement(h, "pose")
                    h2.text = "Unspecified"
                    h3 = ET.SubElement(h, "truncated")
                    h3.text = "0"
                    h4 = ET.SubElement(h, "difficult")
                    h4.text = "0"
                    h5 = ET.SubElement(h, "bndbox")
                    h5_1 = ET.SubElement(h5, "xmin")
                    h5_1.text = str(m)
                    h5_2 = ET.SubElement(h5, "ymin")
                    h5_2.text = str(o)
                    h5_3 = ET.SubElement(h5, "xmax")
                    h5_3.text = str(q)
                    h5_4 = ET.SubElement(h5, "ymax")
                    h5_4.text = str(v)

                    tree = ET.ElementTree(a)  # 创建elementtree对象，写文件
                    tree.write(xmlpath + name + '.xml')

                ########################## 修改XML ###################################
                if i > 0:
                    updateTree = ET.parse(xmlpath + name + '.xml')  # 读取待修改文件
                    annotation = updateTree.getroot()

                    j = ET.Element("object")  # 创建新节点并添加为root的子节点
                    annotation.append(j)  # 更新xml
                    h1 = ET.SubElement(j, "name")
                    h1.text = "bee"
                    h2 = ET.SubElement(j, "pose")
                    h2.text = "Unspecified"
                    h3 = ET.SubElement(j, "truncated")
                    h3.text = "0"
                    h4 = ET.SubElement(j, "difficult")
                    h4.text = "0"
                    h5 = ET.SubElement(j, "bndbox")
                    h5_1 = ET.SubElement(h5, "xmin")
                    h5_1.text = str(m)
                    h5_2 = ET.SubElement(h5, "ymin")
                    h5_2.text = str(o)
                    h5_3 = ET.SubElement(h5, "xmax")
                    h5_3.text = str(q)
                    h5_4 = ET.SubElement(h5, "ymax")
                    h5_4.text = str(v)

                    updateTree.write(xmlpath + name + '.xml')  # 写回原文件

                def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
                    if element:  # 判断element是否有子元素
                        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
                            element.text = newline + indent * (level + 1)
                        else:
                            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (
                                        level + 1)
                            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
                            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
                    temp = list(element)  # 将element转成list
                    for subelement in temp:
                        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                            subelement.tail = newline + indent * (level + 1)
                        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                            subelement.tail = newline + indent * level
                        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

                tree = ElementTree.parse(xmlpath + name + '.xml')  # 解析movies.xml这个文件
                root = tree.getroot()  # 得到根元素，Element类
                pretty_xml(root, '\t', '\n')  # 执行美化方法
                tree.write(xmlpath + name + '.xml')

            #print(fname)
            #imagelist.append(fname)
    if not imagelist:
        print('image not found')
        return

if __name__ == '__main__':
    main()




