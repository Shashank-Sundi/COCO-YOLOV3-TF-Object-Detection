from Log_Writer.logger import App_Logger
import base64
import cv2
logger=App_Logger()

def encodeImage(image):
    try:
        jpg_img = cv2.imencode('.jpeg', image)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        logger.log("Image Converted to Base64 string")
        return b64_string
    except Exception as e:
        logger.log(f"ERROR : Error occurred in decoding base64 string\n")
        logger.log(f"ERROR : {e} \n")
        return print(e)