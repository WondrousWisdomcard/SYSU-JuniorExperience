using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostFactory : MonoBehaviour
{
    private List<GhostData> ghostDatas = new List<GhostData>(); 
    int[] ghostX = new int[4] {-15, -5, 5, 15};
    int[] ghostZ = new int[4] {15, 5, -5, -15};

    // 创建一个幽灵，i（行）j（列）组成房间号， dx dz 是相对于房间中心的位置
    public GameObject GenGhost(int i, int j, int dx, int dz){
        GameObject ghost = Instantiate(Resources.Load<GameObject>("MyPrefabs/Ghost"));
               
        ghost.transform.position = new Vector3(ghostX[i] + dx, 0, ghostZ[j] + dz);
        
        ghost.AddComponent<GhostData>();
        
        ghost.AddComponent<GhostCollideSensor>();

        ghost.transform.GetChild(0).gameObject.AddComponent<InRangeSensor>();
        ghost.transform.GetChild(0).gameObject.GetComponent<InRangeSensor>().ghost = ghost;
    
        GhostData ghostData = ghost.GetComponent<GhostData>();
        ghostData.ghostRoomID = i + j * 4 + 1;
        ghostData.eyeshot = 5;
        ghostData.isInRange = false;
        ghostData.isFollow = false;
        ghostData.isCollided = false;

        ghostDatas.Add(ghostData);

        return ghost;
    }
    
}
