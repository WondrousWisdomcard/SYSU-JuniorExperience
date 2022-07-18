using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostWalkAction : SSAction
{
    private float speed = 0.5F;     // 闲逛速度
    private float GhostX, GhostZ;   // 幽灵位置                 
    private bool turn = true;       // 转向信号

    public GameObject player;       // 玩家对象
    public GameObject ghost;        // 幽灵对象
    private GhostData gData;        // 幽灵数据
    private PlayerData pData;       // 玩家数据

    public static GhostWalkAction GetAction(GameObject player, GameObject ghost) {
        GhostWalkAction action = CreateInstance<GhostWalkAction>();
        action.GhostX = ghost.transform.position.x;
        action.GhostZ = ghost.transform.position.z;
        action.player = player;
        action.ghost = ghost;
        return action;
    }

    public override void Start() {
        gData = ghost.GetComponent<GhostData>();
        pData = player.GetComponent<PlayerData>();
    }

    public override void Update() {

        if (!gData.isFollow && gData.isInRange && gData.ghostRoomID == pData.playerRoomID && !gData.isCollided && pData.alive == true) {
            // 尾随
            this.destroy = true;
            this.enable = false;
            this.callback.SSActionEvent(this);
            this.gameObject.GetComponent<GhostData>().isFollow = true;
            Singleton<GameEventManager>.Instance.FollowPlayer(this.gameObject);
        }
        else {
            // 闲逛
            Walking();
        }
    }

    void Walking() {

        // 随机转向
        if (turn) {
            GhostX = this.transform.position.x + Random.Range(-3F, 3F);
            GhostZ = this.transform.position.z + Random.Range(-3F, 3F);
            this.transform.LookAt(new Vector3(GhostX, 0, GhostZ));
            this.gameObject.GetComponent<GhostData>().isCollided = false;
            turn = false;
        }

        float distance = Vector3.Distance(transform.position, new Vector3(GhostX, 0, GhostZ));

        if (this.gameObject.GetComponent<GhostData>().isCollided) {

            // 碰墙时逆时针旋转120~180度
            this.transform.Rotate(Vector3.up, Random.Range(120, 180));
            GameObject temp = new GameObject();
            temp.transform.position = this.transform.position;
            temp.transform.rotation = this.transform.rotation;
            temp.transform.Translate(0, 0, Random.Range(0.5F, 2F));
            GhostX = temp.transform.position.x;
            GhostZ = temp.transform.position.z;
            this.transform.LookAt(new Vector3(GhostX, 0, GhostZ));
            Destroy(temp);
            this.gameObject.GetComponent<GhostData>().isCollided = false;
            
        } else if (distance <= 0.1F) {
            turn = true;
        } else {
            // 直行
            this.transform.Translate(0, 0, speed * Time.deltaTime);
        }
    }
}
