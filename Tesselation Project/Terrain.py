# COPY THIS CODE TO CREATE A .py FILE TO RUN or COPY TO A JUPYTER (NOT COLAB) NOTEBOOK AND RUN
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:04:11 2020
CSE 30 Spring 2020 Program 1 helper code
@author: Fahim
"""

import math
import turtle
import random

# Note: For this example, we are using hardcoded points/vertices to test the functionalities of the viewer and animation.
# For Program 1, you need to replace the code between the tags # BEGIN and # END with your code.
# Your code should generate the VERTICES and TRIANGLES using your recursive "midpoint_displacement" function.
# This setup is optimized for points values generated in the range -1.00 to 1.00.
# You may need the adjust the value of FOV to generate points with higher ranges.


# BEGIN
# =====================================================================
# Level 0 terrain (1 triangle)

VERTICES = [(-1, 0, 0), (1, 0, 0), (0, 1, 0)]

def randomNumber():
    return random.uniform(0, float(randomDegree))
    return 0

def midpointCalulator(a, b, c):
    #Takes three points as input, then finds midpoints and creates a new triangle

    midpoint1x, midpoint1y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    midpoint2x, midpoint2y = (b[0] + c[0]) / 2, (b[1] + c[1]) / 2
    midpoint3x, midpoint3y = (c[0] + a[0]) / 2, (c[1] + a[1]) / 2

    midpointTraingle = [(midpoint1x, midpoint1y, randomNumber()), (midpoint2x, midpoint2y, randomNumber()), (midpoint3x, midpoint3y, randomNumber())]

    return midpointTraingle

def pointCorrection(VERTICES, midpointList):
    #arranges the midpoints and the exisitng points properly

    VERTICES = [VERTICES[0], midpointList[0], midpointList[2],
                midpointList[0], VERTICES[1], midpointList[1],
                midpointList[2], midpointList[1], VERTICES[2],
                midpointList[0], midpointList[1], midpointList[2]]
    return VERTICES

def triangleReplecation(VERTICES, a, b, c):

    newPoints = midpointCalulator(a, b, c)  #first, calculates the midpoints of the input triangle
    VERTICES += pointCorrection(VERTICES, newPoints) #adds the new triangle and it's points together

    VERTICES.remove(a) #removes the original traingle
    VERTICES.remove(b)
    VERTICES.remove(c)

    if math.log(len(VERTICES)/3, 4).is_integer() != True: #implementation of recursion where it will run until
                                                          #every triangle has been subdivided once only
        triangleReplecation(VERTICES, VERTICES[0], VERTICES[1], VERTICES[2])

    return VERTICES

def zCorrection(VERTICES): #removes the holes in the displacement
    tempVERTICES = []
    for i in range(0, len(VERTICES)):
        for j in range(0, len(VERTICES)):
            if VERTICES[i][0] == VERTICES[j][0] and VERTICES[i][1] == VERTICES[j][1] and VERTICES[i][2] != VERTICES[j][2] and i != j:

                z1, z2 = VERTICES[i][2], VERTICES[j][2]

                z3 = z2


                VERTICES[i] = (VERTICES[i][0],VERTICES[i][1],z3)
                VERTICES[j] = (VERTICES[j][0],VERTICES[j][1],z3)


def transform(x, y, z, angle, tilt):
    # Animation control (around y-axis)
    s, c = math.sin(angle), math.cos(angle)
    x, y = x * c - y * s, x * s + y * c

    # Camera tilt  (around x-axis)
    s, c = math.sin(tilt), math.cos(tilt)
    z, y = z * c - y * s, z * s + y * c

    # Setting up View Parameters
    y += viewAnswer  # Fixed Distance from top
    FOV = 15000  # Fixed Field of view
    f = FOV / y
    sx, sy = x * f, z * f
    return sx, sy

def createTRIANGLESlist(VERTICES):
    #generates the list of verticies automatically based on the point corrections
    finalist = []
    templist = []
    for i in range(0, len(VERTICES)):
        templist.append(i)
        if len(templist) % 3 == 0:
            finalist.append(templist)
            templist = []

    return finalist

#          Parameter that chooses the degree of the recursion
#-----#-----#-----##-----#-----#-----#-----#-----#-----##-----#-----#-----#

recursionLevel = input("Input the desired level of recursion (0-5)")
randomDegree = input("Input the level of displacement (0.0-0.5)")
viewDegree = input("Input desired view (close, mid, far)")

viewAnswer = 0
if(viewDegree == 'close'):
    viewAnswer = 5
elif(viewDegree == 'mid'):
    viewAnswer = 10
elif(viewDegree == 'far'):
    viewAnswer = 15
else:
    print('input not recgonised, default selected (10)')
    viewAnswer = 10

print('Generating Terrain...')

for i in range(0,int(recursionLevel)): #controlls how many triangles are made, 0 = 1, 5 = max
    VERTICES = triangleReplecation(VERTICES, VERTICES[0], VERTICES[1], VERTICES[2])


zCorrection(VERTICES)                          #Removes all holes in the terrain
TRIANGLES = createTRIANGLESlist(VERTICES)      #Draws the triangles between all the others

print('Done!')


# Level 1 terrain (4 pregenerated triangles)
"""VERTICES = [(-1, -0.2, 0), (-0.25, 0, 0), (0, 0, 0.75),
            (0, 0, 0.75), (0.25, 1, 0.75), (-0.25, 0, 0),
            (-0.25, 0, 0), (0, 1, 0), (0.25, 1, 0.75),
            (0.25, 1, 0.75), (1, 0, 0), (0, 0, 0.75)]

TRIANGLES = [(0, 1, 2),
             (3, 4, 5),
             (6, 7, 8),
             (9, 10, 11)]
"""


# =====================================================================
# END




def main():
    # Create terrain using turtle
    terrain = turtle.Turtle()
    terrain.pencolor("blue")
    terrain.pensize(2)

    # Turn off move time for instant drawing
    turtle.tracer(0, 0)
    terrain.up()
    angle = 0

    while True:
        # Clear the screen
        terrain.clear()

        # Transform the terrain
        VERT2D = []
        for vert3D in VERTICES:
            x, y, z = vert3D
            sx, sy = transform(x, y, z, angle, 0.25)
            VERT2D.append((sx, sy))

        # Draw the terrain
        for triangle in TRIANGLES:
            points = []
            points.append(VERT2D[triangle[0]])
            points.append(VERT2D[triangle[1]])
            points.append(VERT2D[triangle[2]])

            # Draw the trangle
            terrain.goto(points[0][0], points[0][1])
            terrain.down()

            terrain.goto(points[1][0], points[1][1])
            terrain.goto(points[2][0], points[2][1])
            terrain.goto(points[0][0], points[0][1])
            terrain.up()

        # Update screen
        turtle.update()

        # Control the speed of animation
        angle += 0.005


if __name__ == "__main__":
    main()
