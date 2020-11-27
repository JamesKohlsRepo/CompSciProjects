// **** Include libraries here ****
// Standard libraries
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h> // For exit() function
#include "Game.h"
//CSE013E Support Library
#include "UNIXBOARD.h"
int GameLoad(int roomNum);


// User libraries


// **** Set any macros or preprocessor directives here ****

// **** Declare any data types here ****

// **** Define any global or external variables here ****

// **** Declare any function prototypes here ****

int main() {
    /******************************** Your custom code goes below here ********************************/
    GameInit();
    int counter;
    char chr;
    char Title[50];
    char Body[500];
    printf("\nWelcome to AdventureLand! type 'q' to exit\n");
    while (1) {

        GameGetCurrentRoomTitle(Title);
        printf("\n - %s - \n\n", Title);

        GameGetCurrentRoomDescription(Body);
        printf("    %s\n", Body);


        int Directions = GameGetCurrentRoomExits();
        printf("Available Directions: ( ");
        if ((Directions & 8) >= 8) {
            printf("NORTH ");
        }
        if ((Directions & 4) >= 4) {
            printf("EAST ");
        }
        if ((Directions & 2) >= 2) {
            printf("SOUTH ");
        }
        if ((Directions & 1) >= 1) {
            printf("WEST ");
        }
        printf(") ");

        if (Directions == 0) {
            printf("\n\nGame Over!\n\n");
            exit(1);
        }
        counter = 0;
        fflush(stdin);
        chr = getchar();
        while (getchar() != '\n') {
            counter++;
        }

        if (counter <= 0) {
            if (chr == 'q') {
                return 0;
            } else if (chr == 'n') {
                GameGoNorth();
            } else if (chr == 'e') {
                GameGoEast();
            } else if (chr == 's') {
                GameGoSouth();
            } else if (chr == 'w') {
                GameGoWest();
            }
        }
    }

    return 0;


    /**************************************************************************************************/
}

