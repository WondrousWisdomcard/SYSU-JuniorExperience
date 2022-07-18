using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostData : MonoBehaviour{
    public int ghostRoomID;         // 幽灵所在房间
    public int eyeshot;             // 幽灵感知半径
    public bool isInRange;          // 是否发现玩家
    public bool isFollow;           // 是否正在追击
    public bool isCollided;         // 是否抓到玩家
}
