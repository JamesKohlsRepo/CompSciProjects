# -*- coding: utf-8 -*-
"""
Created on Thu May 25 04:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Fahim
"""

import numpy as np
import cv2

#Download the required files/sample videos here : https://users.soe.ucsc.edu/~pang/30/s20/prog4/data/
fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
upperbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
lowerbody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture("sample1.avi")
#cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280,720))

while 1:
    count = 0
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = fullbody_cascade.detectMultiScale(gray, 1.3, 5)



    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        upperbody = upperbody_cascade.detectMultiScale(roi_gray)
        lowerbody = lowerbody_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in upperbody:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

        for (ex, ey, ew, eh) in lowerbody:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    cv2.putText(img, "Count: {}".format(count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 3)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()