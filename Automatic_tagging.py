#! /usr/bin/env python
# coding=utf-8

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf

return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0",
                   "pred_lbbox/concat_2:0"]
pb_file = "./yolov3_bee.pb"
dirpath = './VOC2007/JPEGImages/'


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
            print(name + '.jpg')

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
            while i < n:
                bndbox = np.round(bboxes[i])
                # bndbox = int(bnd[:,:4])
                print(int(bndbox[0]), int(bndbox[1]), int(bndbox[2]), int(bndbox[3]))
                xi = int(bndbox[0])
                yi = int(bndbox[1])
                xa = int(bndbox[2])
                ya = int(bndbox[3])

                i = i + 1
            # print(fname)
            # imagelist.append(fname)
    if not imagelist:
        print('image not found')
        return


if __name__ == '__main__':
    main()




