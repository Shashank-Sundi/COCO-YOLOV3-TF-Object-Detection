import tensorflow as tf
import cv2
from Log_Writer.logger import App_Logger
import numpy as np

def process(image):
    try:
        logger = App_Logger()

        image_np = np.array(image)
        logger.log("Image converted to Array")
        if len(image_np.shape) < 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
            logger.log("Image converted from grayscale to rgb")
            # image_np = skimage.color.gray2rgb(image_np)

        # image shape ( height , width , channels)
        # we want it to be ( samples , height , width , channels ) -- for tensorflow
        # for pytorch -- ( samples , channels , height , width )

        # import matplotlib.pyplot as plt
        # plt.imshow(image_np)
        # plt.show()

        return image_np
    except Exception as e:
        logger = App_Logger()
        logger.log("ERROR : Error occurred in preprocessing image\n")
        return print(e)

def transform_images(x_train, size):
    try:
        logger = App_Logger()
        x_train = tf.image.resize(x_train, (size, size))
        x_train = x_train / 255
        logger.log("Image Reshaped Successfully")
    except Exception as e:
        logger = App_Logger()
        logger.log("Error Occured in Reshaping Image")
        print(e)
    return x_train