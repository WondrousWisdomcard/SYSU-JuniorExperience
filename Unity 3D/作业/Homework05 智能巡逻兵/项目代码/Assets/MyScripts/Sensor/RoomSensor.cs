using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoomSensor : MonoBehaviour
{
    FirstController sceneController;

    float[] ghostX = new float[4] {-15F, -5F, 5F, 15F};
    float[] ghostZ = new float[4] {15F, 5F, -5F, -15F};
    float range = 4F;                   // 幽灵移动范围（正方形）的边长

    int tri = 0;
    void Update() {
        sceneController = SSDirector.GetInstance().CurrentSceneController as FirstController;
        
        // 更新玩家所在的房间号
        PlayerUpdate();

        tri++;
        // 降低幽灵的检查频率，避免反复转弯
        if(tri == 20){
            GhostCheck();
            tri = 0;
        }
        
    }

    void PlayerUpdate() {
        GameObject player = sceneController.player;
        Vector3 position = player.transform.position;
        float x = position.x;
        float z = position.z;
        int row = (int) ((x + 20) / 10 + 1);
        int col = (int) (4 - (z + 20) / 10);
        player.GetComponent<PlayerData>().playerRoomID = row + col * 4;
    }

    void GhostCheck() {
        for(int i = 0 ; i < sceneController.ghosts.Count ; i++) {
            GameObject ghost = sceneController.ghosts[i];
            Vector3 gPosition = ghost.transform.position;
            
            // 幽灵的位置
            float gX = gPosition.x;
            float gZ = gPosition.z;

            // 房间对应的行数和列数
            int gRoomID = ghost.GetComponent<GhostData>().ghostRoomID;
            int gRow = (gRoomID - 1) / 4;
            int gCol = (gRoomID - 1) % 4;
            
            // 房间中心的位置
            float cX = ghostX[gCol];
            float cZ = ghostZ[gRow];
            
            if(gX < cX - range || gX > cX + range || gZ < cZ - range || gZ > cZ + range){
                // 如果幽灵尝试离开房间，则视为发生碰撞
                ghost.GetComponent<GhostData>().isCollided = true;
            }
        }
    }
}
