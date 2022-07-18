using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GemData : MonoBehaviour{
    public int gemID;           // 宝石编号
    public int gemRoomID;       // 宝石所在房间
    public bool isValid;        // 是否还存在于地图中
    public bool isCatch;        // 玩家是否碰到宝石
}
