import xml.etree.ElementTree as ET
from xml.etree import ElementTree  # 导入ElementTree模块

########################## 创建xml文件 ################################

a = ET.Element("annotation")       #创建根节点
b = ET.SubElement(a,"folder")  #创建子节点，并添加数据
b.text = "bees"
c = ET.SubElement(a,"filename")  #创建子节点，并添加数据
c.text = "000014.jpg"
d = ET.SubElement(a,"path")  #创建子节点，并添加数据
d.text = "F:/Pythonproject/bee_demo_2/VOC2007/JPEGImages/0000001.jpg"
e = ET.SubElement(a,"source")  #创建子节点，并添加数据
e1 = ET.SubElement(e,"database")
e1.text = "Unknown"
f = ET.SubElement(a,"size")  #创建子节点，并添加数据
f1 = ET.SubElement(f,"width")
f1.text = "2048"
f2 = ET.SubElement(f,"height")
f2.text = "1536"
f3 = ET.SubElement(f,"depth")
f3.text = "3"
g = ET.SubElement(a,"segmented")  #创建子节点，并添加数据
g.text = "0"
h = ET.SubElement(a,"object")  #创建子节点，并添加数据
h1 = ET.SubElement(h,"name")
h1.text = "bee"
h2 = ET.SubElement(h,"pose")
h2.text = "Unspecified"
h3 = ET.SubElement(h,"truncated")
h3.text = "0"
h4 = ET.SubElement(h,"difficult")
h4.text = "0"
h5 = ET.SubElement(h,"bndbox")
h5_1 = ET.SubElement(h5,"xmin")
h5_1.text = "1024"
h5_2 = ET.SubElement(h5,"ymin")
h5_2.text = "1024"
h5_3 = ET.SubElement(h5,"xmax")
h5_3.text = "1024"
h5_4 = ET.SubElement(h5,"ymax")
h5_4.text = "1024"

tree = ET.ElementTree(a)    #创建elementtree对象，写文件
tree.write("test.xml")

########################## 修改XML ###################################

updateTree = ET.parse("test.xml")   # 读取待修改文件
annotation = updateTree.getroot()

j = ET.Element("object")   # 创建新节点并添加为root的子节点
annotation.append(j)                # 更新xml

h1 = ET.SubElement(j,"name")
h1.text = "bee"
h2 = ET.SubElement(j,"pose")
h2.text = "Unspecified"
h3 = ET.SubElement(j,"truncated")
h3.text = "0"
h4 = ET.SubElement(j,"difficult")
h4.text = "0"
h5 = ET.SubElement(j,"bndbox")
h5_1 = ET.SubElement(h5,"xmin")
h5_1.text = "10"
h5_2 = ET.SubElement(h5,"ymin")
h5_2.text = "10"
h5_3 = ET.SubElement(h5,"xmax")
h5_3.text = "10"
h5_4 = ET.SubElement(h5,"ymax")
h5_4.text = "10"


updateTree.write("test.xml")        # 写回原文件

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


tree = ElementTree.parse('test.xml')  # 解析movies.xml这个文件
root = tree.getroot()  # 得到根元素，Element类
pretty_xml(root, '\t', '\n')  # 执行美化方法
tree.write("test.xml")
