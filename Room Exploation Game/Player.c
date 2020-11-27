#ifndef PLAYER_H
#define PLAYER_H

#include "Game.h"
#include "UNIXBOARD.h"
#include <string.h>
// Define how big the player's inventory is.
#define INVENTORY_SIZE 4
#include <stdio.h>
char inventory[255];

/**
 * Adds the specified item to the player's inventory if the inventory isn't full.
 * @param item The item number to be stored: valid values are 0-255.
 * @return SUCCESS if the item was added, STANDARD_ERRROR if the item couldn't be added.
 */
int AddToInventory(uint8_t item) {
    inventory[item] = item;
    //printf("\nAdded %d to inventory\n", item);
    return SUCCESS;
}

/**
 * Check if the given item exists in the player's inventory.
 * @param item The number of the item to be searched for: valid values are 0-255.
 * @return SUCCESS if it was found or STANDARD_ERROR if it wasn't.
 */
int FindInInventory(uint8_t item) {

    if (inventory[item] == item) {
        return SUCCESS;
        //printf("\nFound %d in inventory\n", item);
    } else {
        return STANDARD_ERROR;
    }
    /*
    int d;
    for(d=0;d<strlen(inventory);d++) {
        if(inventory[d] == item){
            printf("you wrote & sign\n");
            return SUCCESS;
        }
    }
    return STANDARD_ERROR;
     */
}

#endif // PLAYER_H

