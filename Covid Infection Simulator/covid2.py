import pygame
import dot
import random

print()
print("Welcome to James Kohls's disease simualtor, Scenario 2, SOCIAL DISTANCING ")
print(" -On day one, 90% of dots will practice social distancing-")
print(" -Immune sprites do not practice social distancing-")
print(" -When dots become sick, they will return home to self isolate-")
print()
print("1) How many people will populate the simulation?")
numberOfpeople = input("    (10-30 yields best results): ")               #Prompts the user for Number of dots
if numberOfpeople == "":                                            #check if nothing has been input
    numberOfpeople = 20                                             #If so it defaults to default values
    numberOfpeople = int(numberOfpeople)                            #for faster testing
else:
    numberOfpeople = int(numberOfpeople)
print("2) how infectious is this disease? ")
infectivity = input("   (1 = 100%, 50 = 50%)): ")
if infectivity == "":
    infectivity = 50
    infectivity = int(infectivity)
else:
    infectivity = int(infectivity)
incubation = input("3) how many days until symptoms become visible?: ")
if incubation == "":
    incubation = 4
    incubation = int(incubation)
else:
    incubation = int(incubation)
incubation = incubation * 2000

lengthofIllness = input("4) how many days will someone be sick?: ")
if lengthofIllness == "":
    lengthofIllness = 7
    lengthofIllness = int(lengthofIllness)
else:
    lengthofIllness = int(lengthofIllness)
lengthofIllness = lengthofIllness * 2000

print("5) how deadly is this disease?")
deadlyness = input("    (1=100%, 2 = 50%): ")
if deadlyness == "":
    deadlyness = 8
    deadlyness = int(deadlyness)
else:
    deadlyness = int(deadlyness)
print()

printTrue = 1
counter = 0
gamewon = 0
covid2 = 1

def randc():
    return (random.randrange(150, 350, 5), random.randrange(150, 350, 5))


pygame.init()                                   # Set up the drawing window
screen = pygame.display.set_mode([500, 500])    # the size of the display
timer  = pygame.time.Clock()                    # creats the clock


all_sprites = pygame.sprite.Group()             # Creates the list of healthy sprites
infected_sprites = pygame.sprite.Group()        # Creates the list of infected sprites
sick_sprites = pygame.sprite.Group()            # Creates the list of Sick sprites
immune_sprites = pygame.sprite.Group()          # Creates the list of Immune sprites
dead_sprites = pygame.sprite.Group()            # Creates the list of Dead Sprites

patientOne = dot.Person((5,250), randc(), (255,165,0), infectivness = infectivity, covid2 = 1, SocialDistancing = 0)     #Patient Zero is generated
infected_sprites.add(patientOne)                                                        #adds to the lisd


for i in range(0, numberOfpeople):
    sd = 0
    randPic = random.randrange(0, 10)  # Determines the Deadliness of the disease
    if randPic <= 9:
        sd = 1
    else:
        sd = 0
    if i <= numberOfpeople/2:
        i = dot.Person((i * int(500/(numberOfpeople/2)), 490), randc(), infectivness = infectivity, SocialDistancing = sd, covid2 =1)
    else:
        i = dot.Person((i * int(500/(numberOfpeople/2))-500, 5), randc(), infectivness = infectivity, SocialDistancing = sd, covid2 =1)

    all_sprites.add(i)          #adds all the healthy sprites to the list

#-------------------------------------------------------
# Runs the simulation

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    all_sprites.update()            # Updates Healthy Dots
    infected_sprites.update()       # Updates Infected Dots
    sick_sprites.update()           # Updates Sick Sprites list
    immune_sprites.update()         # Updates Immune Sprites
    screen.fill((255, 255, 255))    # Fills Screen
    all_sprites.draw(screen)        # Draws Health Sprites
    infected_sprites.draw(screen)   # Draws Infected Sprites
    sick_sprites.draw(screen)       # Draws Sick Sprites
    immune_sprites.draw(screen)     # Draws Immune Sprites

    # Move each dot on the list
    for e in all_sprites:
        all_sprites.draw(screen)
        e.dotSchedule()

    for e in infected_sprites:
        infected_sprites.draw(screen)
        e.dotSchedule()

    for e in sick_sprites:
        sick_sprites.draw(screen)
        e.makeSpriteSick()
        e.dotSchedule()

    for e in immune_sprites:
        immune_sprites.draw(screen)
        e.makeSpriteImmune()
        e.dotSchedule()

    for e in dead_sprites:
        dead_sprites.draw(screen)
        e.makeSpriteDead()
        e.dotSchedule()

    for aPerson in all_sprites:
        all_sprites.remove(aPerson)
        aPerson.collide2(infected_sprites)
        aPerson.collide2(sick_sprites)
        if aPerson.SocialDistancing == 1:
            aPerson.collide2(all_sprites)
        all_sprites.add(aPerson)

        if aPerson.health == 1:
            all_sprites.remove(aPerson)
            infected_sprites.add(aPerson)
            #print('a human has become infected at:', aPerson.timeOfInfection/1000, 'seconds')

    for aPerson in infected_sprites:
        infected_sprites.remove(aPerson)
        aPerson.collide2(all_sprites)
        if aPerson.SocialDistancing == 1:
            aPerson.collide2(infected_sprites)
        infected_sprites.add(aPerson)

        if aPerson.health == 1:
            if pygame.time.get_ticks() - aPerson.timeOfInfection > incubation:       #Determines how long until someone
                infected_sprites.remove(aPerson)                               #develops symptoms
                sick_sprites.add(aPerson)
                #print('a human has fallen ill at:', aPerson.timeOfInfection / 1000, 'seconds')

    for aPerson in sick_sprites:
        sick_sprites.remove(aPerson)
        aPerson.collide2(all_sprites)
        sick_sprites.add(aPerson)

        if aPerson.health == 0:
            if pygame.time.get_ticks() - aPerson.timeOfSymptoms > lengthofIllness:    #Determines the time someone is sick
                randPic = random.randrange(0, deadlyness)                            #Determines the Deadliness of the disease
                if randPic == 0:
                    sick_sprites.remove(aPerson)
                    dead_sprites.add(aPerson)
                else:
                    sick_sprites.remove(aPerson)
                    immune_sprites.add(aPerson)


    #print(pygame.time.get_ticks() % 2000)
    if pygame.time.get_ticks() % 2000 < 10 and len(infected_sprites) + len(sick_sprites) != 0 and printTrue == 1:
        counter += 1
        print('----', 'Day:', counter, '----')
        print('Healthy/Immune:',len(all_sprites) + len(immune_sprites))
        print('Infected/Sick:',len(infected_sprites) + len(sick_sprites))
        print('Dead Sprites:', len(dead_sprites))
        print()
        if len(dead_sprites) > 1:
            print('Mortality Rate:',(len(dead_sprites) / (len(sick_sprites) + len(infected_sprites) + len(immune_sprites) + len(dead_sprites))) * 100, '%')
            print()
        else:
            print('Mortality Rate:', 0, '%')
            print()

    if len(infected_sprites) + len(sick_sprites) == 0 and printTrue == 1:
        if gamewon == 0:
            if (len(all_sprites) + len(immune_sprites) > 0):
                print()
                print('Humanity has survived after', counter, 'days!')
                print('Final mortality rate:',(len(dead_sprites) / (len(sick_sprites) + len(infected_sprites) + len(immune_sprites) + len(dead_sprites))) * 100, '%')
            else:
                print()
                print('Humanity has gone extinct after', counter, 'days')
                print('Final mortality rate:',(len(dead_sprites) / (len(sick_sprites) + len(infected_sprites) + len(immune_sprites) + len(dead_sprites))) * 100, '%')

            gamewon = 1




    # Flip the display
    pygame.display.flip()
    timer.tick(80)

# Done! Time to quit.
pygame.quit()