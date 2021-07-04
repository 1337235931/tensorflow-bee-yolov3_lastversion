import os
import re

# 设置为自己Annotations保存路径
_dir = "../bee_demo/VOC2007/VOC/test/VOCdevkit/VOC2007/Annotations/"
xmlList = os.listdir(_dir)
n = 1
for xml in xmlList:
    # f = open(_dir + xml, "r")
    f = open(_dir + xml, "r", encoding='utf-8')
    xmldata = f.read()
    # 设置为希望修改的path即可
    xmldata = re.sub('\<path>(.*?)\</path>',
                     '<path>F:/Pythonproject/tensorflow-bee-yolov3/VOC2007/Annotations/' + str(n).zfill(7) + '.jpg</path>', xmldata)
    f.close()
    f = open(_dir + xml, "w")
    f.write(xmldata)
    f.close()
    n += 1