# -*- coding: utf-8 -*-
"""
Created on Thu May 25 02:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Fahim
"""

import cv2
import numpy as np
violations = 0

print()
print('-Welcome to the James Kohls Social Distancing checker!-')
print('     -People not within 6ft are in a blue box-')
print('     -People not within 6ft leave a green dot')
print('     -People within 6ft are in a red box-')
print('     -People within 6ft leave a red dot-')
print()
print('-occasionally one person is detected twice so is in violation of social distancing with themselves-')
print('-because of the limitation of not being able to track everyone continosuly, some social distancing violations-')
print('-go unnoticed-')
print()
print('-calibrated with sample1.avi (the only one I had access to)')


fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
upperbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
lowerbody_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture('Sample1.avi')
# cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
# print(frame1.shape)
listOfDots = []

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # print(dilated.shape)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    full_detection = 0
    upper_detection = 0
    lower_detection = 0
    combinedSquare = []
    tooCloseColor = 0,255,0

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        boxes.append((x, y, w, h))
        squaresMade = []



        if cv2.contourArea(contour) < 900:
            continue

        #cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)


        i1 = x
        i2 = x + w
        j1 = y
        j2 = y + h
        #print(i1, i2, j1, j2)
        #print(dilated.shape)
        # exit(0)
        reconstructedImage = frame1[j1:j2, i1:i2]
        #print(reconstructedImage.shape)
        #exit(0)
        #print(reconstructedImage)
        fullbody = fullbody_cascade.detectMultiScale(reconstructedImage, 1.05, 1)
        upperbody = upperbody_cascade.detectMultiScale(reconstructedImage, 1.1, 1)
        lowerbody = lowerbody_cascade.detectMultiScale(reconstructedImage, 1.1, 1)


        #print(len(fullbody))
        for (x, y, w, h) in fullbody:
            full_detection += 1
            #cv2.rectangle(reconstructedImage, (x, y), (x + w, y + h), (255, 255, 0), 2)
            squaresMade.append((x, y, w, h))
            #print(1)
            for (x, y, w, h) in upperbody:
                upper_detection += 1
                #cv2.rectangle(reconstructedImage, (x, y), (x + w, y + h), (255, 0, 0), 2)
                squaresMade.append((x, y, w, h))
                #print(2)
            for (x, y, w, h) in lowerbody:
                lower_detection += 1
                #cv2.rectangle(reconstructedImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
                squaresMade.append((x, y, w, h))

            maxX = 25
            maxY = 25
            maxW = 25
            maxH = 25

            for i in range(0, len(squaresMade)):

                if squaresMade[i][0] < maxX:
                    maxX = squaresMade[i][0]
                if squaresMade[i][1] < maxY:
                    maxY = squaresMade[i][1]
                if squaresMade[i][2] >= maxW:
                    maxW = squaresMade[i][2]
                if squaresMade[i][3] >= maxH:
                    maxH = squaresMade[i][3]

            #print(maxX, maxY, maxX + maxW, maxW + maxH)

            if maxW > squaresMade[0][2]:
                maxW = squaresMade[0][2]

            if maxH > squaresMade[0][3]:
                maxH = squaresMade[0][3]

            combinedSquare.append((i1, j1, maxW, maxH))
            #cv2.rectangle(frame1, (i1, j1), (i1 + maxW, j1 + maxH), (255, 0, 255), 2)
            #listOfDots.append((i1 + 15, j1 + 15), (0,255,0))


        for i in range(0, len(combinedSquare)):
            for j in range(i+1, len(combinedSquare)):

                if abs(combinedSquare[i][0] - combinedSquare[j][0]) > 5:
                    #print('we good')
                    cv2.rectangle(frame1, (combinedSquare[i][0], combinedSquare[i][1]), (
                    combinedSquare[i][0] + combinedSquare[i][2], combinedSquare[i][1] + combinedSquare[i][3]),
                                  (255, 0, 0), 2)
                    listOfDots.append(((i1 + 15, j1 + 15), (0,255,0)))
                else:
                    #print('too mf close')
                    cv2.rectangle(frame1, (combinedSquare[i][0], combinedSquare[i][1]), (
                    combinedSquare[i][0] + combinedSquare[i][2], combinedSquare[i][1] + combinedSquare[i][3]),
                                  (0, 0, 255), 2)
                    listOfDots.append(((i1 + 15, j1 + 15), (0,0,255)))
                    violations +=1

                #print(len(combinedSquare))
                #print(i, j)





            #cv2.circle(frame1, (i1 + 15, j1 + 15), 3, (0, 255, 0), -1)


    #while len(listOfDots) > 100:
        #listOfDots.pop(0)

    #print(len(listOfDots))

    for i in range(0, len(listOfDots)):
        cv2.circle(frame1, listOfDots[i][0], 3, listOfDots[i][1], -1)







    cv2.putText(frame1, "People Detected: {}".format(full_detection + upper_detection + lower_detection), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 0), 2)
    cv2.putText(frame1, "Social Distancing violations: {}".format(violations), (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 0), 2)




    # print()
    # () = method2(box)

    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (640, 480))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()