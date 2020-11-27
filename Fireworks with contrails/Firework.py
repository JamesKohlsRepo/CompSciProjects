# -*- coding: utf-8 -*-
"""
Created on Thu May 08 12:07:14 2020
CSE 30 Spring 2020 Program 3 starter code
@author: Fahim
"""
import random
import pygame
from OpenGL.GL import *
from queue import Queue
from collections import deque
from OpenGL.GLU import *
from pygame.locals import *


class Particle:
    def __init__(self, x=0, y=0, z=0, color=(0, 0, 0, 1)):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.exploded = False
        self.velocity = [random.uniform(-.01, .01), random.uniform(-.01, .01), random.uniform(-.01, .01), ]
        self.tse = 0
        self.q = Queue(maxsize = 15)
        self.listOfParticless = []


    def update(self, ttl):

        #print(self.y)
        if self.y > 10:
            self.exploded = True
        if self.exploded:

            self.listOfParticless.append((self.x, self.y, self.z))        #creates a list of the last 15 locations
            #print(len(self.listOfParticless))
            if len(self.listOfParticless) == 75:                            #creates the secondary explosion
                #print('Popping!')
                self.listOfParticless.pop(0)

            self.tse += 1

            firstX = self.x
            firstY = self.y
            firstZ = self.z
            #listOfThings = []

            originalColor =  self.color[3]
            for i in range(0,len(self.listOfParticless)):

                #print(i,':', self.listOfParticless[i][1])
                #print(self.listOfParticless)
                particle = self.listOfParticless[i]

                self.color = (self.color[0], self.color[1], self.color[2], self.color[3] - (i/20))
                self.x = particle[0]
                #print('new x at', particle[0], 'from', firstX)
                self.y = particle[1]
                #print('new y at', particle[1], 'from', firstY)
                self.z = particle[2]
                #print('new z at', particle[2], 'from', firstZ)
                glColor4fv(self.color)                              #draws comet
                glVertex3fv((self.x, self.y, self.z))




                #print(i)

            #print('---')
            self.color = (self.color[0], self.color[1], self.color[2], originalColor)
            #self.listOfParticless = []


                #print(point1, point2, point3, point4)

                #print(self.q.qsize())

                #xQueue = self.q[i][0]
                #listOfComet = []
                #for i in range (0,0, self.q.qsize()):
                #    i = self.q.get()
                #    listOfComet.append(i)


                #print(listOfComet)

                #self.x = point1[0]
                #self.y = point1[1]
                #self.z = point1[2]

            #self.x = firstX
            #self.y = firstY
            #self.z = firstZ

            self.x += self.velocity[0]
            self.y += self.velocity[1] - 0.5 * (.00000098 * (self.tse * self.tse))            #Projectile motion equation for change in y, time scale decreased for more accuracy due to scale being unknown
            self.z += self.velocity[2]

            #print(self.q.qsize())

            if self.tse > ttl:
                tempTrans = self.color[3]
                tempTrans -= 0.01
                self.color = (self.color[0], self.color[1], self.color[2], tempTrans)
            if self.y < 0:
                tempTrans = 0
                self.color = (self.color[0], self.color[1], self.color[2], tempTrans)
        else:
            self.y += 0.1
            tempTrans = 1
            self.color = (self.color[0], self.color[1], self.color[2], tempTrans)


class Firework(Particle):
    def __init__(self, n, x ,y, z ,ttl, color = (0,0,0,0)):
        self.n = n
        self.x = x
        self.y = y
        self.z = z
        self.ttl = ttl
        self.color = color

        self.listOfParticles = []
        for i in range(0, self.n):

            part = Particle(self.x,self.y,self.z,self.color)
            self.listOfParticles.append(part)

    def render(self):
        glEnable(GL_POINT_SMOOTH)
        glPointSize(3)
        glBegin(GL_POINTS)
        for p in range(len(self.listOfParticles)):
            glColor4fv(self.listOfParticles[p].color)
            glVertex3fv((self.listOfParticles[p].x, self.listOfParticles[p].y, self.listOfParticles[p].z))
            self.listOfParticles[p].update(self.ttl)
        glEnd()



