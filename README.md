识别检测蜜蜂

百度网盘下载权重

链接：https://pan.baidu.com/s/1j1SkT4cFLhIOHh27y7FPBQ 
提取码：g78r

    $ python image_demo.py             # 图片识别
    $ python video_demo.py             # 视频识别   video_path = 0 代表使用摄像头
    
详细训练过程

1.先准备好数据集，VOC2007格式默认，再通过使用算法产生anchors（也可以采用默认的anchors）
$ python anchors_generate.py

2.产生训练数据txt文件
$ python split.py

    train.txt 里面应该像这样:
        xxx/xxx.jpg 18.19,6.32,424.13,421.83,20 323.86,2.65,640.0,421.94,20 
        xxx/xxx.jpg 48,240,195,371,11 8,12,352,498,14
    解读:
        image_path x_min, y_min, x_max, y_max, class_id  x_min, y_min ,..., class_id 
        x_min, y_min etc. corresponds to the data in XML files

3.修改names文件
  voc.names文件
  person
  bicycle
  car
  ...
  toothbrush

4.正式训练: 修改 config.py 文件，主要根据显存大小，注意batch_size，输入尺寸等参数
$ python train.py
$ python train_mobilenetv2.py   # 注意anchors 最好使用coco_anchors
$ tensorboard --logdir ./data/log    # 查看损失等变化曲线

如果想使用 mobilenetv2 backbone ，请运行：
$ python freeze_graph.py
$ python freeze_graph_mobilenetv2.py

预测,修改 路径等相关参数:
修改 image_demo.py, config.py等文件
$ python image_demo.py
$ python image_demo_mobilenetv2.py
