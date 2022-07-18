using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerFactory : MonoBehaviour
{
    private PlayerData playerData;
    public GameObject GenPlayer(){

        GameObject player = Instantiate(Resources.Load<GameObject>("MyPrefabs/JohnLemon"));
        
        player.AddComponent<PlayerController>();
        player.AddComponent<PlayerData>();
        playerData = player.GetComponent<PlayerData>();

        
        // 开始房间：7
        playerData.playerRoomID = 7;
        playerData.alive = true;

        return player;
    }
    
}
