

#include <stdint.h>
#include "Message.h"
#include "BattleBoats.h"
#include "Field.h"
#include "BattleBoats.h"

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
#include "OledDriver.h"
#include "FieldOled.h"

// Battleboats Libraries:
#include "BattleBoats.h"
#include "Agent.h"
#include "Negotiation.h"
#include "Message.h"
#include "Field.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "BOARD.h"
#include <xc.h>
#include <sys/attribs.h>
#include "Agent.h"
#include "Negotiation.h"
#include "Field.h"
#include <string.h>
#include <math.h>

/**
 * Defines the various states used within the agent state machines. All states should be used
 * within a valid agent implementation. Additionally there is no need for states outside of
 * those defined here.
 */


typedef struct {
    int roundCounter;
    AgentState agentState;        
    NegotiationData PlayerA;
    NegotiationData PlayerB;
    NegotiationData PlayerAHash;
} Agent;

static Agent agent;

/**
 * The Init() function for an Agent sets up everything necessary for an agent before the game
 * starts.  At a minimum, this requires:
 *   -setting the start state of the Agent SM.
 *   -setting turn counter to 0
 * If you are using any other persistent data in Agent SM, that should be reset as well.
 * 
 * It is not advised to call srand() inside of AgentInit.  
 *  */
void AgentInit(void){
    agent.agentState = AGENT_STATE_START;
    agent.roundCounter = 0;

    agent.PlayerA = 0;
    agent.PlayerB = 0;
    agent.PlayerAHash = 0;
}

static Field myField;
static Field theirField;
static Message message;
static GuessData yourGuess, theirGuess; 


/**
 * AgentRun evolves the Agent state machine in response to an event.
 * 
 * @param  The most recently detected event
 * @return Message, a Message struct to send to the opponent. 
 * 
 * If the returned Message struct is a valid message
 * (that is, not of type MESSAGE_NONE), then it will be
 * passed to the transmission module and sent via UART.
 * This is handled at the top level! AgentRun is ONLY responsible 
 * for generating the Message struct, not for encoding or sending it.
 */
Message AgentRun(BB_Event event){
    
    
    
    if (event.type == BB_EVENT_RESET_BUTTON){
        agent.agentState = AGENT_STATE_START;
        agent.roundCounter = 1;
        agent.PlayerA = 0;
        agent.PlayerB = 0;
        agent.PlayerAHash = 0;
        
        OledClear(0);
        OledDrawString("This is BattleBoats!\nPress BTN4 to\nchallenge, or wait\nfor opponent.");
        OledUpdate();
        
        agent.agentState = AGENT_STATE_START;
    }
    message.param0 = 0;
    message.param1 = 0;
    message.param2 = 0;
    message.type = MESSAGE_NONE;
    
    switch(agent.agentState) {
            case(AGENT_STATE_START):
                if(event.type == BB_EVENT_START_BUTTON){
                    FieldInit(&myField,&theirField);
                    FieldAIPlaceAllBoats(&myField);
                    
                    OledClear(0);
                    OledDrawString("Challenge Sent to:\nPlayer2");
                    OledUpdate();

                    agent.PlayerA = rand() % 15;
                    agent.PlayerAHash = NegotiationHash(agent.PlayerA);

                    agent.agentState = AGENT_STATE_CHALLENGING;
                    message.type = MESSAGE_CHA;
                    message.param0 = agent.PlayerAHash;
                    return message;
                }
                if(event.type == BB_EVENT_CHA_RECEIVED){
                    FieldInit(&myField,&theirField);
                    FieldAIPlaceAllBoats(&myField);
                    
                    OledClear(0);
                    OledDrawString("Challenge Received\nfrom: Player2");
                    OledUpdate();
                    
                    agent.PlayerB = rand() % 15;
                    agent.PlayerAHash = event.param0;

                    message.type = MESSAGE_ACC; 
                    message.param0 = agent.PlayerB;
                    
                    agent.agentState = AGENT_STATE_ACCEPTING; 
                    return message;
                }
                break;
            case(AGENT_STATE_CHALLENGING):
                
                if(event.type == BB_EVENT_ACC_RECEIVED){
                    OledClear(0);
                    OledDrawString("ACCEPTED RECIVED.\n");
                    OledUpdate();
                    message.type = MESSAGE_REV;
                    //message.param0 = agent.PlayerA;
                    if (NegotiateCoinFlip(agent.PlayerA, agent.PlayerB) == HEADS) {
                        agent.agentState = AGENT_STATE_WAITING_TO_SEND;
                        OledClear(0);
                        OledDrawString("Coinflip Results:\nHEADS");
                        OledUpdate();
                    } else if (NegotiateCoinFlip(agent.PlayerA, agent.PlayerB) == TAILS){
                        agent.agentState = AGENT_STATE_DEFENDING;
                        OledClear(0);
                        OledDrawString("Coinflip Results:\nTAILS");
                        OledUpdate();
                    }
                    
                } else {
                    message.type = MESSAGE_NONE;
                    return message;
                }
                
                break;
            case(AGENT_STATE_ACCEPTING):
                
                if(event.type == BB_EVENT_REV_RECEIVED){
                    agent.PlayerA = event.param0;
                    if (NegotiateCoinFlip(agent.PlayerA, agent.PlayerB) == HEADS) {
                        agent.agentState = AGENT_STATE_DEFENDING;
                        OledClear(0);
                        OledDrawString("Coinflip Results:\nHEADS");
                        OledUpdate();
                    } else if (NegotiateCoinFlip(agent.PlayerA, agent.PlayerB) == TAILS) {
                        OledClear(0);
                        OledDrawString("Coinflip Results:\nTAILS");
                        OledUpdate();
                        yourGuess = FieldAIDecideGuess(&theirField);
                        message.param0 = yourGuess.row;
                        message.param1 = yourGuess.col;
                        //message.param2 = yourGuess.result;
                        agent.agentState = AGENT_STATE_ATTACKING;
                        message.type = MESSAGE_SHO;
                    }
                    return message;
                }
                break;
            case(AGENT_STATE_ATTACKING):  
                
                if(event.type == BB_EVENT_RES_RECEIVED){
                    
                    OledClear(0);
                    OledDrawString("ATTACK!\n");
                    OledUpdate();
                    
                    yourGuess.row = event.param0;
                    yourGuess.col = event.param1;
                    yourGuess.result = event.param2;
                    FieldUpdateKnowledge(&theirField, &yourGuess);
                    
                    
                    if (FieldGetBoatStates(&theirField) == 0){
                        agent.agentState = AGENT_STATE_END_SCREEN;
                        OledClear(0);
                        OledDrawString("DEFEAT.");
                        OledUpdate();
                    } else {
                        agent.agentState = AGENT_STATE_DEFENDING;
                    }
                    return message;
                }
                message.type = MESSAGE_NONE;
                return message;
                break;
            case(AGENT_STATE_DEFENDING):
                
                if(event.type == BB_EVENT_SHO_RECEIVED){
                    
                    OledClear(0);
                    OledDrawString("DEFEND!\n");
                    OledUpdate();
                    
                    theirGuess.row = event.param0;
                    theirGuess.col = event.param1;
                    FieldRegisterEnemyAttack(&myField, &theirGuess);
                    theirGuess.result = event.param2;
                    
                    message.param0 = theirGuess.row;
                    message.param1 = theirGuess.col;
                    message.param2 = theirGuess.result;
                    message.type = MESSAGE_RES;
                    
                    if (FieldGetBoatStates(&myField) == 0){
                        agent.agentState = AGENT_STATE_END_SCREEN;
                        OledClear(0);
                        OledDrawString("VICTORY.");
                        OledUpdate();
                    } else {
                        agent.agentState = AGENT_STATE_WAITING_TO_SEND;
                    }
                    message.type = MESSAGE_RES;
                    return message;
                } else {
                    message.type = MESSAGE_NONE;
                    return message;
                }
                break;
            case(AGENT_STATE_WAITING_TO_SEND):
                if(event.type == BB_EVENT_MESSAGE_SENT){
                    OledClear(0);
                    char str[80];
                    sprintf(str, " -BattleBoats-\n Round number: %d", agent.roundCounter);
                    OledDrawString(str);
                    OledUpdate();
                    
                    agent.roundCounter += 1;
                    yourGuess = FieldAIDecideGuess(&theirField);
                    
                    message.param0 = yourGuess.row;
                    message.param1 = yourGuess.col;
                    message.param2 = yourGuess.result;
                    message.type = MESSAGE_SHO;
                    agent.agentState = AGENT_STATE_ATTACKING;
                    return message;
                } else {
                    message.type = MESSAGE_NONE;
                    return message;
                }
                break;
            case(AGENT_STATE_END_SCREEN):
                break;
            case(AGENT_STATE_SETUP_BOATS):
                break;

    }
    return message;
}


/** * 
 * @return Returns the current state that AgentGetState is in.  
 * 
 * This function is very useful for testing AgentRun.
 */
AgentState AgentGetState(void){
    AgentState state = agent.agentState;
    return state;
}

/** * 
 * @param Force the agent into the state given by AgentState
 * 
 * This function is very useful for testing AgentRun.
 */
void AgentSetState(AgentState newState){
    agent.agentState = newState;
}


