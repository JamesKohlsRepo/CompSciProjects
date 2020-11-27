import random
import pygame
import Firework
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

print()
print('Welcome to the James Kohls Fireworks Simulator!')
print(' -Fireworks will have secondary explosions- ')
print(' -Comet trails begin once fireworks have begun their decent- ')
print(' -The fireworks display is composed of five fireworks circa the example- ')
print(' -Apologies for the lag - ')



def terrain():
    ''' Draws a simple square as the terrain '''
    glBegin(GL_QUADS)
    glColor4fv((0, 0, 1, 1))  # Colors are now: RGBA, A = alpha for opacity
    glVertex3fv((10, 0, 10))  # These are the xyz coords of 4 corners of flat terrain.
    glVertex3fv((-10, 0, 10))  # If you want to be fancy, you can replace this method
    glVertex3fv((-10, 0, -10))  # to draw the terrain from your prog1 instead.
    glVertex3fv((10, 0, -10))
    glEnd()

def main():

    pygame.init()

    # Set up the screen
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Firework Simulation")
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, -5, -25)
    #glRotatef(10, 2, 1, 0)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_BLEND);

    play = True
    sim_time = 0

    # A clock object for keeping track of fps
    clock = pygame.time.Clock()

    #( 10 (# of particles), 0,0,0 (coordinates) , 300 (time to live), (0,0,0,1), color ))

    f1 = Firework.Firework(10, 0, 0, 0, 300, (random.random(), random.random(), random.random(), 1))
    f2 = Firework.Firework(10, -5, 0, 5, 300,(1, 0, 0, 1))
    f3 = Firework.Firework(10, -5, 0, -5, 300,(random.random(), random.random(), random.random(), 1))
    f4 = Firework.Firework(10, 5, 0, -5, 200,(0, 1, 0, 1))
    f5 = Firework.Firework(10, 5, 0, 5, 100,(random.random(), random.random(), random.random(), 1))

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(10, 0, 1, 0)

                if event.key == pygame.K_UP:
                    glRotatef(-10, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(10, 1, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        glRotatef(0.10, 0, 1, 0)
        # glTranslatef(0, 0.1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        terrain()

        if 100 < sim_time <= 1000:
            f1.render()   # f1 is one firework
        if 500 < sim_time <= 1500:
            f2.render()  # f1 is one firework
            f3.render()  # f1 is one firework
        if 1000 < sim_time <= 1500:
            f4.render()  # f1 is one firework
            f5.render()  # f1 is one firework
        if 1500 < sim_time:
            sim_time = 0
            print('new')



        pygame.display.flip()
        sim_time += 1
        clock.tick(150)

    pygame.quit()


if __name__ == "__main__":
    main()