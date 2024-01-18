from ultralytics import YOLO
import cv2
import math 
import logging
import requests
import time

logging.basicConfig(level=logging.INFO, format="%(name)s: %(asctime)s - %(levelname)s - %(message)s")
logging.info(f"[+] Starting {__name__}")


# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

model = YOLO("models/yolov8n.pt")

r_headers ={
    "content-type": "application/json", 
    'API-KEY': "1234567890"
}
mainloop_endpoint = "http://127.0.0.1:8888/MODULE_object_detection"


# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush",
              ]

def main():
    logging.info("Starting object recognition module")
    
    while True:
        time.sleep(0.2)
        try:
            requests.post(mainloop_endpoint, headers=r_headers, json={"test": "200"})
            break
        except Exception:
            logging.debug("Waiting for flask server to start")
        
    while True:
        success, img = cap.read()        
        results = model(img, verbose=False)

        requests_form = {
            "class": [],
            "confidence": []
        }
        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0]*100))/100

                # class name
                cls = int(box.cls[0])
                requests_form["class"].append(classNames[cls])
                requests_form["confidence"].append(confidence)
            

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                
                
        object_reco_r = requests.post(
            mainloop_endpoint, 
            json={"class": requests_form["class"], "confidence": requests_form["confidence"]}, 
            headers=r_headers)
               
        logging.debug(f"{object_reco_r.status_code}")
        
        
        cv2.imshow('preview', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.warning("Stopping object recognition module")
    

