from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from Log_Writer.logger import App_Logger
from Base64.Decoder import decodeImage
from Base64.Encoder import encodeImage
from Preprocess.preprocessor import process , transform_images
from yolov3_tf2.models import YoloV3
from yolov3_tf2.utils import draw_outputs
import numpy as np
import cv2


app = Flask(__name__)
CORS(app)

logger = App_Logger()

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def homePage():
    try:
        logger.log("Rendered Home Page Successfully")
        return render_template('index.html')
    except Exception as e:
        return print(e)

@app.route('/detections', methods=['POST'])
@cross_origin()
def index():
    try:
        if request.method == 'POST':

            # Collect BAse64 string
            base64 = request.form['image']
            logger.log("Collected Base64 string")

            # Decode base64 string & get PIL image
            image = decodeImage(base64)

            # Convert to Image array & then to tensor & preprocess
            original_image=process(image)
            image = original_image[np.newaxis, :]

            # load in weights in Model and classes
            yolo = YoloV3(classes=80)
            yolo.load_weights('./weights/yolov3.tf').expect_partial()
            class_names = [c.strip() for c in open('./data/labels/coco.names').readlines()]
            image = transform_images(image, 416)
            boxes, scores, classes, nums = yolo(image)

            for i in range(nums[0]):
                print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                            np.array(scores[0][i]),
                                            np.array(boxes[0][i])))

            # Overlay BB on image
            img = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
            img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
            cv2.imwrite('./detections/detection.jpg', img)
            print('output saved to: {}'.format('./detections/' + 'detection.jpg'))

            # Convert Image to Base64
            base64=encodeImage(img)


            logger.log("Prediction Successful")
            return render_template("results.html", base64=base64)
        else:
            logger.log("Did not get POST request\n")
            return render_template("index.html")
    except Exception as e:
        logger.log("ERROR : Some Error Occurred\n")
        return print(f"Error : {e}")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8001)
