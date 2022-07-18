using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainSceneController : MonoBehaviour, ISceneController, IUserAction
{
    
    Vector3 riverPosition = new Vector3(0,0,0); // 10 X 10 X 1
    Vector3 leftBankPosition = new Vector3(-35,0,0); // 10 X 10 X 1.2
    Vector3 rightBankPosition = new Vector3(35,0,0); // 10 X 10 X 1.2
    Vector3 boatStartPosition = new Vector3(5,0,0); // 2 X 4 X 0.5
    Vector3 boatDestinationPosition = new Vector3(-5,0,0); 
    Vector3[] characterInitPosition = new Vector3[6];

    GameObject river, leftBank, rightBank;
    BoatModel boatModel;
    CharacterModel[] priests = new CharacterModel[3];
    CharacterModel[] devils = new CharacterModel[3];

    SceneGUI sceneGUI;

    void Awake(){
        Debug.Log("Preparing...");
        Director director = Director.getInstance();
        director.currentSceneController = this;
        director.currentSceneController.loadResources();
        sceneGUI = gameObject.AddComponent (typeof(SceneGUI)) as SceneGUI;
    }

    void generateGameObjects(){
        // River
        river = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/River"), riverPosition, Quaternion.identity);
        river.name = "River";

        // The Bank
        leftBank = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/RiverBank"), leftBankPosition, Quaternion.identity);
		leftBank.name = "DestBank";
        rightBank = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/RiverBank"), rightBankPosition, Quaternion.identity);
		rightBank.name = "StartBank";
        
        // Boat
        boatModel = new BoatModel(boatStartPosition, boatDestinationPosition);

        // Priests & Devils
        for(int i = 0; i < 6; i++){
            characterInitPosition[i] = rightBankPosition + Vector3.right * (i * 1.2F - 2 - 25);
        }

        priests[0] = new CharacterModel(CharacterModel.PRIEST, "Justica", characterInitPosition[0]);
        priests[1] = new CharacterModel(CharacterModel.PRIEST, "Kindmes", characterInitPosition[1]);
        priests[2] = new CharacterModel(CharacterModel.PRIEST, "Loyalti", characterInitPosition[2]);

        devils[0] = new CharacterModel(CharacterModel.DEVIL, "Gred", characterInitPosition[3]);
        devils[1] = new CharacterModel(CharacterModel.DEVIL, "Arroganca", characterInitPosition[4]);
        devils[2] = new CharacterModel(CharacterModel.DEVIL, "Lazi", characterInitPosition[5]);
    }

    public void loadResources(){
        Debug.Log("Loading resources...");
        generateGameObjects();
    }

    public void gameRestart(){
        Debug.Log("Restart game...");
        boatModel.resetBoat();
        for(int i = 0; i < 3; i++){
            priests[i].resetCharacter();
            devils[i].resetCharacter();
        }
    }

    public void clickCharacter(CharacterModel characterModel){
        if(characterModel.getCharacterType() == CharacterModel.PRIEST){
            Debug.Log("Priest clicked");
        }
        else if(characterModel.getCharacterType() == CharacterModel.DEVIL){
            Debug.Log("Devil clicked");
        }

        if(characterModel.getCharacterState() == CharacterModel.ASHORE_START && boatModel.getBoatState() == BoatModel.PARKING_START){
            // StartBank 上船
            if(boatModel.getEmptySitsCount() != 0){
                characterModel.moveCharacterPosition(boatModel.getASit(characterModel), Moveable.EMBARK);
                characterModel.setCharacterState(CharacterModel.ONBOARD);
            } 
        }
        else if(characterModel.getCharacterState() == CharacterModel.ASHORE_DESTINATION && boatModel.getBoatState() == BoatModel.PARKING_DESTINATION){
            // DestinationBank 上船
            if(boatModel.getEmptySitsCount() != 0){
                characterModel.moveCharacterPosition(boatModel.getASit(characterModel), Moveable.EMBARK);
                characterModel.setCharacterState(CharacterModel.ONBOARD);
            }
        }
        else if(characterModel.getCharacterState() == CharacterModel.ONBOARD){
            if(boatModel.getBoatState() == BoatModel.PARKING_START){ 
                // StartBank 下船
                boatModel.leaveASit(characterModel);
                characterModel.moveCharacterPosition(characterModel.getInitialPosition(), Moveable.DISEMBARK);
                characterModel.setCharacterState(CharacterModel.ASHORE_START);

            }
            else if(boatModel.getBoatState() == BoatModel.PARKING_DESTINATION){
                // DestinationBank 下船
                boatModel.leaveASit(characterModel);
                characterModel.moveCharacterPosition(characterModel.getInitialPosition() - Vector3.right * 2 * characterModel.getInitialPosition().x, Moveable.DISEMBARK);
                characterModel.setCharacterState(CharacterModel.ASHORE_DESTINATION);
            }
        }

    }

    public void clickBoat(BoatModel boatModel){
        Debug.Log("Boat clicked");
        if(boatModel.getOccupiedSitsCount() != 0){
            if(boatModel.getBoatState() == BoatModel.PARKING_START){
                // StartBank -> DestinationBank
                boatModel.moveBoatPosition(boatModel.getDestinationPosition(), Moveable.SHIPING);
                boatModel.setBoatState(BoatModel.PARKING_DESTINATION);
            }
            else if(boatModel.getBoatState() == BoatModel.PARKING_DESTINATION){
                // DestinationBank -> StartBank
                boatModel.moveBoatPosition(boatModel.getStartPosition(), Moveable.SHIPING);
                boatModel.setBoatState(BoatModel.PARKING_START);
            }
        }
    }

    void Update(){
        if(sceneGUI.getUnlock() ==  true){
            gameJudge();
        }
    }

    public void gameJudge(){
        int startDevilNum = 0, destinationDevilNum = 0;
        int startPriestNum = 0, destinationPriestNum = 0;

        if(boatModel.getMoveableCurrentState() == Moveable.SHIPING){
            return;
        }

        for(int i = 0; i < 3; i++){
            if(priests[i].getCharacterState() == CharacterModel.ASHORE_START){
                startPriestNum++;
            }
            else if(priests[i].getCharacterState() == CharacterModel.ASHORE_DESTINATION){
                destinationPriestNum++;
            }

            if(devils[i].getCharacterState() == CharacterModel.ASHORE_START){
                startDevilNum++;
            }
            else if(devils[i].getCharacterState() == CharacterModel.ASHORE_DESTINATION){
                destinationDevilNum++;
            }
        }

        if(boatModel.getOccupiedSitsCount() != 0){
            if(boatModel.getBoatState() == BoatModel.PARKING_START){
                startPriestNum = 3 - destinationPriestNum;
                startDevilNum = 3 - destinationDevilNum;
            }
            else if(boatModel.getBoatState() == BoatModel.PARKING_DESTINATION){
                destinationPriestNum = 3 - startPriestNum;
                destinationDevilNum = 3 - startDevilNum;
            }
        }

        if((startPriestNum != 0 && startPriestNum < startDevilNum) || (destinationPriestNum != 0 && destinationPriestNum < destinationDevilNum)){
            Debug.Log("Game Over");
            sceneGUI.setGameState(SceneGUI.LOSE);
        }

        if(destinationPriestNum == 3 && destinationDevilNum == 3){
            Debug.Log("You Win");
            sceneGUI.setGameState(SceneGUI.WIN);
        }

    }
}
