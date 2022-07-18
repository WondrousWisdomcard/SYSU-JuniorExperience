using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostActionManager : SSActionManager, ISSActionCallback
{
    public GhostWalkAction walk;
    public GhostFollowAction follow;

    // 闲逛
    public void Walk(GameObject player, GameObject ghost) {
        this.walk = GhostWalkAction.GetAction(player, ghost);
        this.RunSSAction(ghost, walk, this);
    }

    // 追击
    public void Follow(GameObject player, GameObject ghost) {
        this.follow = GhostFollowAction.GetAction(player, ghost);
        this.RunSSAction(ghost, follow, this);
    }

    // 停止
    public void DestroyAllActions() {
        DestroyAll();
    }

    public void SSActionEvent(SSAction source, SSActionEventType events = SSActionEventType.Completed, int intParam = 0, string strParam = null, Object objectParam = null) {

    }
}
