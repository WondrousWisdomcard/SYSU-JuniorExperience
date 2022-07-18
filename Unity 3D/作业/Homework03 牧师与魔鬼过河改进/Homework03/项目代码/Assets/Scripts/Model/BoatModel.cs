using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoatModel
{
    private GameObject boat;
    private BoatGUI boatGUI;
    private Vector3 startPosition, destinationPosition;

    private int boatState;
    
    private int[] sits = new int[2];
    private CharacterModel[] characters = new CharacterModel[2];
    private static int EMPTY_SIT = 0;
    private static int OCCUPIED_SIT = 1;

    public static int SHIPING = 0;
    public static int PARKING_DESTINATION = 1;
    public static int PARKING_START = 2;

    public BoatModel(Vector3 startPosition, Vector3 destinationPosition){
        this.boatState = PARKING_START;

        boat = Object.Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/Boat"), Vector3.zero, Quaternion.identity);
        boat.name = "Boat";

        boat.transform.position = startPosition;
        this.startPosition = startPosition;
        this.destinationPosition = destinationPosition;
        boatGUI = boat.AddComponent (typeof(BoatGUI)) as BoatGUI;
        boatGUI.SetBoatGUI(UserGUI.BOAT, this);

        sits[0] = sits[1] = EMPTY_SIT;
    }

    public int getOccupiedSitsCount(){
        int num = 0;
        for(int i = 0; i < 2; i++){
            if(sits[i] == OCCUPIED_SIT){
                num++;
            }
        }
        return num;
    }
    public int getEmptySitsCount(){
        return 2 - getOccupiedSitsCount();
    }

    public Vector3 getASit(CharacterModel character){
        for(int i = 0; i < 2; i++){
            if(sits[i] == EMPTY_SIT){
                character.getGameObject().transform.parent = boat.transform;
                sits[i] = OCCUPIED_SIT;
                characters[i] = character;
                if(character.getCharacterState() == CharacterModel.ASHORE_START){
                    return getStartPosition() - Vector3.right * 0.6F + Vector3.right * 1.2F * i;
                }
                else if(character.getCharacterState() == CharacterModel.ASHORE_DESTINATION){
                    return getDestinationPosition() - Vector3.right * 0.6F + Vector3.right * 1.2F * i;
                }
               
            }
        }
        return character.getInitialPosition();
    }

    public void leaveASit(CharacterModel character){
        for(int i = 0; i < 2; i++){
            if(characters[i] == character){
                sits[i] = EMPTY_SIT;
                character.getGameObject().transform.parent = null;
                characters[i] = null;
            }
        }
    }

    public void setBoatState(int boatState){
        this.boatState = boatState;
    }

    public int getBoatState(){
        return boatState;
    }

    public void setBoatPosition(Vector3 position){
        boat.transform.position = position;
    }

    public Vector3 getStartPosition(){
        return startPosition;
    }
    public Vector3 getDestinationPosition(){
        return destinationPosition;
    }

    public GameObject getGameObject(){
        return boat;
    }

    public void resetBoat(){
        boatState = PARKING_START;
        setBoatPosition(startPosition);
        for( int i = 0; i < 2; i++){
            sits[i] = EMPTY_SIT;
            if(characters[i] != null){
                characters[i].getGameObject().transform.parent = null;
                characters[i] = null;
            }
        }
    }
    
}
