using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Referee{
    MainSceneController controller;
    
    public Referee(){
        controller = (MainSceneController)Director.getInstance().currentSceneController;
    } 

    public int gameJudge(){
        int startDevilNum = 0, destinationDevilNum = 0;
        int startPriestNum = 0, destinationPriestNum = 0;

        for(int i = 0; i < 3; i++){
            if(controller.priests[i].getCharacterState() == CharacterModel.ASHORE_START){
                startPriestNum++;
            }
            else if(controller.priests[i].getCharacterState() == CharacterModel.ASHORE_DESTINATION){
                destinationPriestNum++;
            }

            if(controller.devils[i].getCharacterState() == CharacterModel.ASHORE_START){
                startDevilNum++;
            }
            else if(controller.devils[i].getCharacterState() == CharacterModel.ASHORE_DESTINATION){
                destinationDevilNum++;
            }
        }

        if(controller.boat.getOccupiedSitsCount() != 0){
            if(controller.boat.getBoatState() == BoatModel.PARKING_START){
                startPriestNum = 3 - destinationPriestNum;
                startDevilNum = 3 - destinationDevilNum;
            }
            else if(controller.boat.getBoatState() == BoatModel.PARKING_DESTINATION){
                destinationPriestNum = 3 - startPriestNum;
                destinationDevilNum = 3 - startDevilNum;
            }
        }

        if((startPriestNum != 0 && startPriestNum < startDevilNum) || (destinationPriestNum != 0 && destinationPriestNum < destinationDevilNum)){
            Debug.Log("Game Over");
            return -1;
        }

        if(destinationPriestNum == 3 && destinationDevilNum == 3){
            Debug.Log("You Win");
            return 1;
        }

        return 0;
    }
}