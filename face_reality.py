from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from os.path import dirname, join
from PIL import Image
import numpy as np
import logging
import imutils
import pickle
import base64
import pickle
import time
import cv2
import io
import os

net = cv2.dnn.readNetFromCaffe(join(dirname(__file__), "face_detector/deploy.prototxt"),
                               join(dirname(__file__), "face_detector/res10_300x300_ssd_iter_140000.caffemodel"))

model = load_model(join(dirname(__file__), "face_detector/liveness.model"))

le = pickle.loads(
    open(join(dirname(__file__), "face_detector/le.pickle"), "rb").read())


def _base64_to_image(base_string):
    base_string = base64.b64decode(base_string)
    base_string = io.BytesIO(base_string)
    base_string = Image.open(base_string)
    base_string = base_string.convert('RGB')
    base_string = np.array(base_string)
    base_string = base_string[:, :, ::-1].copy()

    return base_string


class CheckReality:
    def __init__(self, frame):
        self.frame = frame

    def return_label(self):
        placeHolder = {
            "real": 1,
            "fake": 0
        }

        frame = _base64_to_image(self.frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        frame = imutils.resize(frame, width=600)

        (h, w) = frame.shape[: 2]
        blob = cv2.dnn.blobFromImage(cv2.resize(
            frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if len(detections) > 0:
                i = np.argmax(detections[0, 0, :, 2])
                confidence = detections[0, 0, i, 2]

                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    face = frame[startY:endY, startX:endX]

                    startX = max(0, startX)
                    startY = max(0, startY)
                    endX = min(w, endX)
                    endY = min(h, endY)

                    face = frame[startY:endY, startX:endX]
                    face = cv2.resize(face, (32, 32))
                    face = face.astype("float") / 255.0
                    face = img_to_array(face)
                    face = np.expand_dims(face, axis=0)

                    preds = model.predict(face)[0]
                    j = np.argmax(preds)
                    label = le.classes_[j]

                    logging.info(label)

                    return placeHolder[label]
