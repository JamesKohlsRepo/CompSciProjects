// **** Include libraries here ****
// Standard libraries
#include <stdio.h>
#include <string.h>
#include <stdint.h>

//CMPE13 Support Library
#include "BOARD.h"

// Microchip libraries
#include <xc.h>
#include <sys/attribs.h>

//CE13 standard libraries:
#include "Buttons.h"
#include "Uart1.h"
#include "Oled.h"

// Battleboats Libraries:
#include "BattleBoats.h"
#include "Agent.h"
#include "Negotiation.h"
#include "Message.h"
#include "Field.h"
#include <time.h>   



int main(){
    BOARD_Init();
    TRISE = 0;
    LATE = 0;

    //initialize CE13 libraries:
    //ButtonsInit();
    OledInit();
    //Print a greeting:
    int a;
    AgentState state;
    int b = 0;
    BB_Event message;
    //message.type = BB_EVENT_START_BUTTON;
    
    
    
    printf("1) RUN AGENT INIT\n");
    AgentInit();
    printf(" -Success!\n");
    
    printf("2) BEGIN ROUND CYCLE\n");
    message.type = BB_EVENT_START_BUTTON;
    AgentRun(message);
    state = AgentGetState();
    printf("  -State START");
    printf("  -State Number: %d\n",state);
    for(a = 0; a<600000; a++);
    message.type = BB_EVENT_ACC_RECEIVED;
    AgentRun(message);
    state = AgentGetState();
    printf("  -State CHALLENGING");
    printf("  -State Number: %d\n",state);
    for(a = 0; a<600000; a++);
    message.type = BB_EVENT_SHO_RECEIVED;
    AgentRun(message);
    state = AgentGetState();
    if (state == 5) {printf("  -State WAITING TO SEND");} else if(state == 4) {printf("  -State DEFENDING");}
    printf("  -State Number: %d\n",state);
    for(a = 0; a<600000; a++);
    
    printf("3) ENTER ATTACK/DEFEND CYCLE (60 rounds)\n");
    while(b < 60){
    message.type = BB_EVENT_MESSAGE_SENT;
    AgentRun(message);
    state = AgentGetState();
    if (state == 5) {printf("  -State WAITING TO SEND");} else if(state == 4) {printf("  -State DEFENDING");} else if(state == 3) {printf("  -State ATTACKING");}
    printf("  -State Number: %d\n",state);
    for(a = 0; a<100000; a++);
    message.type = BB_EVENT_RES_RECEIVED;
    AgentRun(message);
    state = AgentGetState();
    if (state == 5) {printf("  -State WAITING TO SEND");} else if(state == 4) {printf("  -State DEFENDING");} else if(state == 3) {printf("  -State ATTACKING");}
    printf("  -State Number: %d\n",state);
    for(a = 0; a<100000; a++);
    message.type = BB_EVENT_SHO_RECEIVED;
    AgentRun(message);
    state = AgentGetState();
    if (state == 5) {printf("  -State WAITING TO SEND");} else if(state == 4) {printf("  -State DEFENDING");} else if(state == 3) {printf("  -State ATTACKING");}
    printf("  -State Number: %d\n",state);
    for(a = 0; a<100000; a++);
    b++;
    printf("-ROUND NUMBER %d-\n", b);
    }
    
    printf("4) RESET THE GAME\n");
    
    message.type = BB_EVENT_RESET_BUTTON;
    AgentRun(message);
    printf(" -Success!\n");
    state = AgentGetState();
    printf("  -State START");
    printf("  -State Number: %d\n",state);
    for(a = 0; a<600000; a++);
    
    printf("4) SETTING STATES\n");
    printf(" -set state to AGENT_STATE_ACCEPTING\n");
    AgentSetState(AGENT_STATE_ACCEPTING);
    state = AgentGetState();
    if (state == 2){printf("  -state change successful!\n");} else{printf("-state change failed!\n");}
    
    printf(" -set state to AGENT_STATE_END_SCREEN\n");
    AgentSetState(AGENT_STATE_END_SCREEN);
    state = AgentGetState();
    if (state == 6){printf("  -state change successful!\n");} else{printf("-state change failed!\n");}
    
}

