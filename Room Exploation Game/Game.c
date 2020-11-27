#ifndef GAME_H
#define GAME_H
#include <stdio.h>
#include <stdlib.h> // For exit() function
#include "UNIXBOARD.h"
#include "Player.h"
#include <stdio.h>
#include <stdlib.h> // For exit() function
#include <stdint.h>
#include <string.h>
int GameLoad(int roomNum);

// The initial room that Game should initialize to.
#define STARTING_ROOM 32



// These variable describe the maximum string length of the room title and description respectively.
// Note that they don't account for the trailing '\0' character implicit with C-style strings.
#define GAME_MAX_ROOM_TITLE_LENGTH 21
#define GAME_MAX_ROOM_DESC_LENGTH 255

/**
 * This enum defines flags for checking the return values of GetCurrentRoomExits(). Usage is as
 * follows:
 *
 * if (GetCurrentRoomExits() & GAME_ROOM_EXIT_WEST_EXISTS) {
 *   // The current room has a west exit.
 * }
 *
 * @see GetCurrentRoomExits
 */
typedef enum {
    GAME_ROOM_EXIT_WEST_EXISTS = 0b0001,
    GAME_ROOM_EXIT_SOUTH_EXISTS = 0b0010,
    GAME_ROOM_EXIT_EAST_EXISTS = 0b0100,
    GAME_ROOM_EXIT_NORTH_EXISTS = 0b1000
} GameRoomExitFlags;

typedef struct roomData {
    int titleLenght;
    int bodyLength;
    int itemRequirementLength;
    int itemReceivedLength;
    int north;
    int south;
    int east;
    int west;

    char title[50];
    char body[500];

    int loadSecondRoomOption;

} roomInfo;

roomInfo room;

/**
 * These function transitions between rooms. Each call should return SUCCESS if the current room has
 * an exit in the correct direction and the new room was able to be loaded, and STANDARD_ERROR
 * otherwise.
 * @return SUCCESS if the room CAN be navigated to and changing the current room to that new room
 *         succeeded.
 */
int GameGoNorth(void) {
    if (room.north != 0) {
        GameLoad(room.north);
        return SUCCESS;
    } else {
        return STANDARD_ERROR;
    }
}

/**
 * @see GameGoNorth
 */
int GameGoEast(void) {
    if (room.east != 0) {
        GameLoad(room.east);
        return SUCCESS;
    } else {
        return STANDARD_ERROR;
    }
}

/**
 * @see GameGoNorth
 */
int GameGoSouth(void) {
    if (room.south != 0) {
        GameLoad(room.south);
        return SUCCESS;
    } else {
        return STANDARD_ERROR;
    }
}

/**
 * @see GameGoNorth
 */
int GameGoWest(void) {
    if (room.west != 0) {
        GameLoad(room.west);
        return SUCCESS;
    } else {
        return STANDARD_ERROR;
    }
}

/**
 * This function sets up anything that needs to happen at the start of the game. This is just
 * setting the current room to STARTING_ROOM and loading it. It should return SUCCESS if it succeeds
 * and STANDARD_ERROR if it doesn't.
 * @return SUCCESS or STANDARD_ERROR
 */
int GameInit(void) {
    return GameLoad(STARTING_ROOM);
}

/**
 * Copies the current room title as a NULL-terminated string into the provided character array.
 * Only a NULL-character is copied if there was an error so that the resultant output string
 * length is 0.
 * @param title A character array to copy the room title into. Should be GAME_MAX_ROOM_TITLE_LENGTH+1
 *             in length in order to allow for all possible titles to be copied into it.
 * @return The length of the string stored into `title`. Note that the actual number of chars
 *         written into `title` will be this value + 1 to account for the NULL terminating
 *         character.
 */
int GameLoad(int roomNum) {
    //function takes the room number passed to it, then breaks down the file into useful data
    FILE *fptr;
    char roomName[50];
    sprintf(roomName, "RoomFiles/room%d.txt", roomNum);
    if ((fptr = fopen(roomName, "rb")) == NULL) {
        return STANDARD_ERROR;
        exit(1); // Program exits if file pointer returns NULL.
    }

    // First, this finds the length of the title after RPG
    fseek(fptr, 3, SEEK_CUR);
    room.titleLenght = fgetc(fptr);
    //printf("Length of Title: %d\n", j); 

    // This function gets the title of the Room
    fseek(fptr, 4, SEEK_SET);
    fgets(room.title, (room.titleLenght + 1), fptr);


    // Finds the number of items needed to access a room
    fseek(fptr, 0, SEEK_CUR);
    room.itemRequirementLength = fgetc(fptr);
    //printf("Items Required: %d\n", i); 
    // if there is one or more item that is available, they are cycled through
    if (room.itemRequirementLength != 0) {
        int i2;
        for (int x = 0; x < room.itemRequirementLength; x++) {
            fseek(fptr, 0, SEEK_CUR);
            i2 = fgetc(fptr);
            if (FindInInventory(i2) == SUCCESS) {
                room.loadSecondRoomOption = 0;
            } else {
                room.loadSecondRoomOption = 1;
            }
        }
    }

    // Gets the length of the body text
    fseek(fptr, 0, SEEK_CUR);
    room.bodyLength = fgetc(fptr);

    //Gets the body text into room.body
    //fseek adds the length of the variables and name before it, then adds 6 for the plus ones, and the RPG
    fseek(fptr, (room.titleLenght + room.itemRequirementLength + 6), SEEK_SET);
    fgets(room.body, (room.bodyLength + 1), fptr);

    // Gets the number of items available for pickup in a room, stores them in the inventory (eventually)
    fseek(fptr, 0, SEEK_CUR);
    room.itemRequirementLength = fgetc(fptr);
    //printf("Items you can pickup: %d\n", q); 
    if (room.itemRequirementLength != 0) {
        int q2;
        for (int x = 0; x < room.itemRequirementLength; x++) {
            fseek(fptr, 0, SEEK_CUR);
            q2 = fgetc(fptr);
            AddToInventory(q2);
        }
    }

    fseek(fptr, 0, SEEK_CUR); // checking NORTH
    room.north = fgetc(fptr);

    fseek(fptr, 0, SEEK_CUR); // checking EAST
    room.east = fgetc(fptr);

    fseek(fptr, 0, SEEK_CUR); // checking SOUTH
    room.south = fgetc(fptr);

    fseek(fptr, 0, SEEK_CUR); // checking WEST
    room.west = fgetc(fptr);

    //logic to save the second part
    if (room.loadSecondRoomOption == 1) {
        fseek(fptr, 0, SEEK_CUR);
        room.itemRequirementLength = fgetc(fptr);
        fseek(fptr, 0, SEEK_CUR);
        room.bodyLength = fgetc(fptr);
        fseek(fptr, 0, SEEK_CUR);
        fgets(room.body, (room.bodyLength + 1), fptr);
        fseek(fptr, 0, SEEK_CUR);
        room.itemRequirementLength = fgetc(fptr);
        //printf("Items you can pickup: %d\n", q); 

        // Gets the number of items available for pickup in a room, stores them in the inventory (eventually)
        if (room.itemRequirementLength != 0) {
            int q2;
            for (int x = 0; x < room.itemRequirementLength; x++) {
                fseek(fptr, 0, SEEK_CUR);
                q2 = fgetc(fptr);
                AddToInventory(q2);
            }
        }
    }


    fclose(fptr);

    return (0);
}

int GameGetCurrentRoomTitle(char *title) {
    strcpy(title, room.title);
    return room.titleLenght;

}

/**
 * GetCurrentRoomDescription() copies the description of the current room into the argument desc as
 * a C-style string with a NULL-terminating character. The room description is guaranteed to be less
 * -than-or-equal to GAME_MAX_ROOM_DESC_LENGTH characters, so the provided argument must be at least
 * GAME_MAX_ROOM_DESC_LENGTH + 1 characters long. Only a NULL-character is copied if there was an
 * error so that the resultant output string length is 0.
 * @param desc A character array to copy the room description into.
 * @return The length of the string stored into `desc`. Note that the actual number of chars
 *          written into `desc` will be this value + 1 to account for the NULL terminating
 *          character.
 */
int GameGetCurrentRoomDescription(char *desc) {
    strcpy(desc, room.body);
    return room.bodyLength;
}

/**
 * This function returns the exits from the current room in the lowest-four bits of the returned
 * uint8 in the order of NORTH, EAST, SOUTH, and WEST such that NORTH is in the MSB and WEST is in
 * the LSB. A bit value of 1 corresponds to there being a valid exit in that direction and a bit
 * value of 0 corresponds to there being no exit in that direction. The GameRoomExitFlags enum
 * provides bit-flags for checking the return value.
 *
 * @see GameRoomExitFlags
 *
 * @return a 4-bit bitfield signifying which exits are available to this room.
 */
uint8_t GameGetCurrentRoomExits(void) {
    int returnValue = 0;

    if (room.north != 0) {
        returnValue += 8;
    }
    if (room.east != 0) {
        returnValue += 4;
    }
    if (room.south != 0) {
        returnValue += 2;
    }
    if (room.west != 0) {
        returnValue += 1;
    }

    return returnValue;
}

#endif // GAME_H

