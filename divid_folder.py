# coding=gbk
import os
from shutil import copyfile
#根据tarin.txt和test.txt将数据集分为标准数据集
train_text_path = 'F:/Pythonproject/tensorflow-bee-yolov3/VOC2007/ImageSets/Main/train.txt'
test_text_path = 'F:/Pythonproject/tensorflow-bee-yolov3/VOC2007/ImageSets/Main/test.txt'
#图片存放地址
image_path = 'F:/Pythonproject/tensorflow-bee-yolov3/VOC2007/JPEGImages'
#xml文件存放地址
xml_path = 'F:/Pythonproject/tensorflow-bee-yolov3/VOC2007/Annotations'

#输出的目录
outdir = 'F:/Pythonproject/tensorflow-bee-yolov3/VOC2007'
#创建各级文件夹
test_xml_out = os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/Annotations')
os.makedirs(test_xml_out)
os.makedirs(os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/ImageSets/Layout'))
os.makedirs(os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/ImageSets/Main'))
os.makedirs(os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/ImageSets/Segmentation'))
test_img_out = os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/JPEGImages')
os.makedirs(test_img_out)
os.makedirs(os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/SegmentationClass'))
os.makedirs(os.path.join(outdir,'VOC/test/VOCdevkit/VOC2007/SegmentationObject'))
train_xml_out = os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/Annotations')
os.makedirs(train_xml_out)
os.makedirs(os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/ImageSets/Layout'))
os.makedirs(os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/ImageSets/Main'))
os.makedirs(os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/ImageSets/Segmentation'))
train_img_out = os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/JPEGImages')
os.makedirs(train_img_out)
os.makedirs(os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/SegmentationClass'))
os.makedirs(os.path.join(outdir,'VOC/train/VOCdevkit/VOC2007/SegmentationObject'))



with open(train_text_path) as f:
    lines = f.readlines()
    for i in lines:
        img_save_path = os.path.join(train_img_out,i.rstrip('\n')+'.jpg')
        xml_save_path = os.path.join(train_xml_out, i.rstrip('\n') + '.xml')
        copyfile(os.path.join(image_path,i.rstrip('\n')+'.jpg'),img_save_path)
        copyfile(os.path.join(xml_path, i.rstrip('\n') + '.xml'), xml_save_path)
        print(i)
with open(test_text_path) as f:
    lines = f.readlines()
    for i in lines:
        img_save_path = os.path.join(test_img_out, i.rstrip('\n') + '.jpg')
        xml_save_path = os.path.join(test_xml_out, i.rstrip('\n') + '.xml')
        copyfile(os.path.join(image_path, i.rstrip('\n') + '.jpg'), img_save_path)
        copyfile(os.path.join(xml_path, i.rstrip('\n') + '.xml'), xml_save_path)
        print(i)
