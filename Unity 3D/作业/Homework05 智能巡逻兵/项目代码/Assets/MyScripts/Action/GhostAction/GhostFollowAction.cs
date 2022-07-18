using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostFollowAction : SSAction
{
    private float speed = 0.8F;     // 追击速度（玩家的速度是 1F）
    public GameObject player;       // 玩家对象
    public GameObject ghost;        // 幽灵对象
    private GhostData gData;        // 幽灵数据
    private PlayerData pData;       // 玩家数据

    public static GhostFollowAction GetAction(GameObject player, GameObject ghost) {
        GhostFollowAction action = CreateInstance<GhostFollowAction>();
        action.player = player;
        action.ghost = ghost;
        return action;
        
    }

    public override void Start() {
        gData = ghost.GetComponent<GhostData>();
        pData = player.GetComponent<PlayerData>();
    }

    public override void Update() {
        
        if (gData.isFollow && (!gData.isInRange || gData.ghostRoomID != pData.playerRoomID || gData.isCollided || pData.alive == false)) {
            // 放弃跟随
            this.destroy = true;
            this.enable = false;
            this.callback.SSActionEvent(this);
            this.gameObject.GetComponent<GhostData>().isFollow = false;
            Singleton<GameEventManager>.Instance.PlayerEscape(this.gameObject);
        }
        else {
            // 尾随
            Following();
        }
    }

    void Following() {
        // 面向玩家
        transform.LookAt(player.transform.position);
        // 跟随玩家
        transform.position = Vector3.MoveTowards(this.transform.position, player.transform.position, speed * Time.deltaTime);
    }
}
