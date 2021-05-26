# cam.py
# this is from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="my_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

face_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

# the index depends on your camera setup and which one is your USB camera.
# you may need to change to 1 depending on your local config
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    # cv2.imshow('frame', gray)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        gray_img = gray[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        _,msg_to_send = cv2.imencode('.png', gray_img)
        bin_msg = msg_to_send.tobytes()
        #publish the message
        print("face detected: ")
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, bin_msg)
        print("published mesg")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
