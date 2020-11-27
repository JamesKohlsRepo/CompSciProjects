import numpy
import random
import pygame
import pygame.gfxdraw

healthyPerson_IMG = pygame.Surface((10, 10), pygame.SRCALPHA)        #health sprite
pygame.gfxdraw.aacircle(healthyPerson_IMG, 4, 4, 4, (0, 0, 255))
pygame.gfxdraw.filled_circle(healthyPerson_IMG, 4, 4, 4, (0, 0, 255))

sickPerson_IMG = pygame.Surface((10, 10), pygame.SRCALPHA)        #Sick sprite
pygame.gfxdraw.aacircle(sickPerson_IMG, 4, 4, 4, (255, 165, 0))
pygame.gfxdraw.filled_circle(sickPerson_IMG, 4, 4, 4, (255, 165, 0))

illPerson_IMG = pygame.Surface((10, 10), pygame.SRCALPHA)        #Sick sprite
pygame.gfxdraw.aacircle(illPerson_IMG, 4, 4, 4, (255, 0, 0))
pygame.gfxdraw.filled_circle(illPerson_IMG, 4, 4, 4, (255, 0, 0))

immunePerson_IMG = pygame.Surface((10, 10), pygame.SRCALPHA)        #Immune sprite
pygame.gfxdraw.aacircle(immunePerson_IMG, 4, 4, 4, (0, 255, 0))
pygame.gfxdraw.filled_circle(immunePerson_IMG, 4, 4, 4, (0, 255, 0))

deadPerson_IMG = pygame.Surface((10, 10), pygame.SRCALPHA)        #Dead sprite
pygame.gfxdraw.aacircle(deadPerson_IMG, 4, 4, 4, (0, 0, 0))
pygame.gfxdraw.filled_circle(deadPerson_IMG, 4, 4, 4, (0, 0, 0))

#-------------------------------------------------------------------

healthyPerson2_IMG = pygame.image.load("healthysprite.png")      #health sprite

sickPerson2_IMG = pygame.image.load("infectedsprite.png")        #infected sprite

illPerson2_IMG = pygame.image.load("sicksprite.png")        #Sick sprite

immunePerson2_IMG = pygame.image.load("immunesprite.png")      #Immune sprite

deadPerson2_IMG = pygame.Surface((20, 20), pygame.SRCALPHA)        #Dead sprite
pygame.gfxdraw.aacircle(deadPerson2_IMG, 8, 8, 8, (0, 0, 0))
#pygame.gfxdraw.filled_circle(deadPerson_IMG, 4, 4, 4, (0, 0, 0))

class Person(pygame.sprite.Sprite):
    def __init__(self, start=(0, 0), end=(0, 0), color=(0, 0, 255), health = 2, timeOfInfection = 0, timeOfSymptoms = 0, infectivness = 0, SocialDistancing = 0, covid2 =0, covid3 = 0):

        self.start = start  # P0
        self.gps = start  # position along the line
        self.goal = end  # P1
        self.color = color
        self.size = 5
        self.isNearOtherPerson = 0
        self.health = health
        self.timeOfInfection = timeOfInfection
        self.timeOfSymptoms = timeOfSymptoms
        self.infectivness = infectivness
        self.home = 0
        self.SocialDistancing = SocialDistancing
        self.covid2 = covid2
        self.covid3 = covid3

        pygame.sprite.Sprite.__init__(self)
        if covid2 == 0:
            if self.color == (0, 0, 255):
                self.image = healthyPerson_IMG
                self.health = 2
            elif self.color == (255, 165, 0):
                self.image = sickPerson_IMG
                self.health = 1
            elif self.color == (255, 0, 0):
                self.image = illPerson_IMG
                self.health = 0
            elif self.color == (0, 255, 0):
                self.image = immunePerson_IMG
                self.health = 3
                self.home = 0
            else:
                self.image = deadPerson_IMG
                self.health = -1
        else:
            if self.color == (0, 0, 255):
                self.image = healthyPerson2_IMG
                self.health = 2
            elif self.color == (255, 165, 0):
                self.image = sickPerson2_IMG
                self.health = 1
            elif self.color == (255, 0, 0):
                self.image = illPerson2_IMG
                self.health = 0
            elif self.color == (0, 255, 0):
                self.image = immunePerson2_IMG
                self.health = 3
                self.home = 0
            else:
                self.image = deadPerson2_IMG
                self.health = -1

        self.rect = self.image.get_rect(width = 15, height = 15)
        # self.rect.center = (255, 255)

    def move(self):  # "diagonal" move 1 step closer to goal

        if self.health == 0:            #checks if the dot is feeling sick, and should stay home
            if self.gps == self.start and (self.start[1] == 490 or self.start[1] == 5 or self.start == (5,250)):
                self.home = 1

        if self.health == 3:
            self.home = 0

        sx = numpy.sign(self.goal[0] - self.gps[0])  # returns -1,0,1
        nx = self.gps[0] + sx
        sy = numpy.sign(self.goal[1] - self.gps[1])
        ny = self.gps[1] + sy
        if self.gps != self.goal:
            self.gps = (nx, ny)
        else:
            t = self.start
            self.start = self.goal
            self.goal = t

    def moveManhattan(self):

        if self.health == 0:  # checks if the dot is feeling sick, and should stay home
            if self.gps == self.start and (self.start[1] == 490 or self.start[1] == 5 or self.start == (5, 250)):
                self.home = 1

        if self.health == 3:
            self.home = 0


        # write code to move from start_pos to end_pos in hor/ver
        sx = numpy.sign(self.goal[0] - self.gps[0])  # returns -1,0,1
        if sx:
            self.gps = (self.gps[0] + sx, self.gps[1])
        else:
            sy = numpy.sign(self.goal[1] - self.gps[1])
            self.gps = (self.gps[0], self.gps[1] + sy)

        if self.gps == self.goal:
            t = self.start
            self.start = self.goal
            self.goal = t

    def moveLine(self):
        # write code to move in straight line
        dx = self.goal[0] - self.start[0]
        # sx = numpy.sign(dx)  # returns -1,0,1
        nx = round(self.gps[0] + 0.01 * dx)

        dy = self.goal[1] - self.start[1]
        # sy = numpy.sign(dy)
        ny = round(self.gps[1] + 0.01 * dy)
        self.gps = (int(nx), int(ny))

        if self.gps == self.goal:
            t = self.start
            self.start = self.goal
            self.goal = t


    def dotSchedule(self):

        if self.home == 0 or self.health == 3:
            self.moveManhattan()
            self.move()

    def determineStyle(self):
        randPic = random.randrange(0, 2)  # pick a random movement dicision
        if randPic == 0:
            t = self.start
            self.start = self.goal
            self.goal = t

    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self, spriteGroup, False):
            randPic = random.randrange(0, self.infectivness)                  #Determines the infectivness of the disease
            if randPic == 0:
                self.timeOfInfection = pygame.time.get_ticks()
                self.health = 1
                if self.covid2 == 0:
                    self.image = sickPerson_IMG
                else:
                    self.image = sickPerson2_IMG

    def collide2(self, spriteGroup):

        if self.SocialDistancing == 1:
            collisions = pygame.sprite.spritecollide(self, spriteGroup, False)

            if len(collisions) > 0:
                testString = [self.gps]
                for j in collisions:
                    testString.append(j.gps)
            if len(collisions) >= 1:

                if (self.health == 1 or self.health == 0 or collisions[0].health == 0 or collisions[0].health == 1):
                    self.collide(spriteGroup)

                xValueDifference = abs(self.gps[0] - collisions[0].gps[0])
                yValueDifference = abs(self.gps[1] - collisions[0].gps[1])

                if xValueDifference > yValueDifference:
                    if self.gps[0] < collisions[0].gps[0]:
                        self.gps = (self.gps[0], self.gps[1] + 6)
                        collisions[0].gps = (collisions[0].gps[0], collisions[0].gps[1]- 6)
                        self.determineStyle()
                    else:
                        self.gps = (self.gps[0], self.gps[1] - 6)
                        collisions[0].gps = (collisions[0].gps[0], collisions[0].gps[1] + 6)
                        self.determineStyle()
                if yValueDifference > xValueDifference:
                    if self.gps[1] < collisions[0].gps[1]:
                        self.gps = (self.gps[0]+ 6, self.gps[1])
                        collisions[0].gps = (collisions[0].gps[0]- 6, collisions[0].gps[1])
                        self.determineStyle()
                    else:
                        self.gps = (self.gps[0] - 6, self.gps[1])
                        collisions[0].gps = (collisions[0].gps[0] + 6, collisions[0].gps[1])
                        self.determineStyle()

                #print(xValueDifference, yValueDifference)

    def makeSpriteSick(self):
        if self.health != 0:
            if self.covid2 == 0:
                self.image = illPerson_IMG
            else:
                self.image = illPerson2_IMG
            self.health = 0
            self.timeOfSymptoms = pygame.time.get_ticks()

    def makeSpriteImmune(self):
        if self.health != 3:
            if self.covid2 == 0:
                self.image = immunePerson_IMG
            else:
                self.image = immunePerson2_IMG
            if self.start == self.goal:
                self.goal = (random.randrange(150, 350, 5), random.randrange(150, 350, 5))
            self.health = 3

    def makeSpriteDead(self):
        if self.health != -1:
            self.image = deadPerson_IMG
            self.health = -1

    def update(self):

        #clock = pygame.time.Clock()
        #print(self.gps)
        self.rect.x = self.gps[0]
        self.rect.y = self.gps[1]
