using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 管理游戏时间，参考：https://gitee.com/Enrique518/unity3d_hw/tree/master/Intelligent%20Patrol/Assets/Scripts
public class GameEventManager : MonoBehaviour
{
    // 玩家逃脱事件
    public delegate void EscapeEvent(GameObject ghost);
    public static event EscapeEvent OnGoalLost;
    // 巡逻兵追击事件
    public delegate void FollowEvent(GameObject ghost);
    public static event FollowEvent OnFollowing;
    // 游戏失败事件
    public delegate void GameOverEvent();
    public static event GameOverEvent GameOver;
    // 游戏胜利事件
    public delegate void WinEvent();
    public static event WinEvent Win;

    // 获取宝石事件
    public delegate void GemEvent(GameObject gem);
    public static event GemEvent OnGettingGem;

    // 玩家逃脱
    public void PlayerEscape(GameObject ghost) {
        if (OnGoalLost != null) {
            OnGoalLost(ghost);
        }
    }

    // 获得水晶
    public void GettingGem(GameObject gem) {
        if(OnGettingGem != null){
            OnGettingGem(gem);
        }
    }

    // 幽灵追击
    public void FollowPlayer(GameObject ghost) {
        if (OnFollowing != null) {
            OnFollowing(ghost);
        }
    }

    // 玩家被抓
    public void OnPlayerCatched() {
        if (GameOver != null) {
            GameOver();
        }
    }

}
