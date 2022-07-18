using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GemFactory : MonoBehaviour
{
    private List<GemData> gems = new List<GemData>();

    string gemsPath = "MyPrefabs/Gem/Gem";
    string[] gemsID = new string[11] {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"};

    int[] gemX = new int[4] {-15, -5, 5, 15};
    int[] gemZ = new int[4] {15, 5, -5, -15};

    // 返回指定房间内的宝石
    public GameObject GetGem(int roomID){
        if(gems.Count != 0){
            foreach(GemData existGem in gems){
                if(existGem.gemRoomID == roomID){
                    return existGem.gameObject;
                }
            }
        }
        return null;
    }

    // 创建指定ID和房间的宝石
    public GameObject GenGem(int gemID, int roomID){

        GameObject gem = null;
        
        // 给出宝石的预制路径、根据房间ID算出位置和Quaternion
        string gemPath = gemsPath + gemsID[gemID];
        int x = gemX[(roomID - 1) % 4];
        int z = gemZ[(roomID - 1) / 4];
        Vector3 pos = new Vector3(x, 1, z);
        Quaternion rot = new Quaternion(-0.707106829F, 0, 0, 0.707106829F);

        // 创建宝石对象
        gem = GameObject.Instantiate<GameObject>(Resources.Load<GameObject>(gemPath), pos, rot);
        
        // 创建碰撞检测器
        gem.AddComponent<GemCollideSensor>();

        // 为创建的宝石对象赋予数据
        gem.AddComponent<GemData>();
        if(gem != null){
            GemData gemData = gem.GetComponent<GemData>();
            gemData.gemID = gemID;
            gemData.gemRoomID = roomID;
            gemData.isValid = true;
            gemData.isCatch = false;
            gems.Add(gemData);
        }
        gem.SetActive(true);
        return gem;
    }

    // 删除宝石
    public void FreeGem(GameObject gem){
        foreach(GemData gemData in gems){
            if(gemData.gameObject.GetInstanceID() == gem.GetInstanceID()){
                gem.SetActive(false);
                gems.Remove(gemData);
                break;
            }
        }
    }
    void Update() {
        
    }
}
