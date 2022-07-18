using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DiskFactory : MonoBehaviour
{
    private List<DiskData> busyDisks;
    private List<DiskData> freeDisks;

    string[] Prefabs = new string[5] {"Prefabs/YellowDisk", 
        "Prefabs/GreenDisk", "Prefabs/CyanDisk", 
        "Prefabs/BlueDisk", "Prefabs/BlackDisk"};

    // Start is called before the first frame update
    void Start()
    {
        busyDisks = new List<DiskData>();
        freeDisks = new List<DiskData>();
    }

    public GameObject GetDisk(int level){
        GameObject disk = null;

        bool find = false;
        for(int i = 0; i < freeDisks.Count; i++){
            if(freeDisks[i].level == level){
                disk = freeDisks[i].gameObject;
                freeDisks.RemoveAt(i);
                find = true;
                break;
            }
        }
        
        if(find == false){
            disk = GameObject.Instantiate<GameObject>(Resources.Load<GameObject>(Prefabs[level - 1]), Vector3.zero, Quaternion.identity);
            disk.AddComponent<DiskData>();
            disk.AddComponent<Rigidbody>();
            disk.AddComponent<ConstantForce>();
        }

        if(disk != null){
            DiskData diskData = disk.GetComponent<DiskData>();
            setDiskData(diskData, level);
            busyDisks.Add(diskData);
        }

        return disk;
    }

    public void FreeDisk(GameObject disk){
        foreach(DiskData diskData in busyDisks){
            if(diskData.gameObject.GetInstanceID() == disk.GetInstanceID()){
                disk.SetActive(false);
                busyDisks.Remove(diskData);
                freeDisks.Add(diskData);
                break;
            }
        }
    }

    public void setDiskData(DiskData diskData, int level){
        if(level <= 1){
            diskData.level = 1;
            diskData.mass = 1.0F + Random.Range(-1F, 1F) * 0.4F;
            diskData.score = 50;
            diskData.speed = new Vector3(Random.Range(-0.1F, 0.1F), Random.Range(-0.1F, 0.1F), Random.Range(-0.1F, 0.1F));
            diskData.force = new Vector3(Random.Range(-1F, 1F), Random.Range(-1F, 1F), Random.Range(-1F, 1F));
        }
        else if(level == 2){
            diskData.level = 2;
            diskData.mass = 2.0F + Random.Range(-1F, 1F) * 0.8F;
            diskData.score = 100;
            diskData.speed = new Vector3(Random.Range(-2F, 2F), Random.Range(-2F, 2F), Random.Range(-2F, 2F));
            diskData.force = new Vector3(Random.Range(-2F, 2F), Random.Range(-2F, 2F), Random.Range(-2F, 2F));
        }
        else if(level == 3){
            diskData.level = 3;
            diskData.mass = 3.0F + Random.Range(-1F, 1F) * 1.6F;
            diskData.score = 500;
            diskData.speed = new Vector3(Random.Range(-5F, 5F), Random.Range(-5F, 5F), Random.Range(-5F, 5F));
            diskData.force = new Vector3(Random.Range(-5F, 5F), Random.Range(-5F, 5F), Random.Range(-5F, 5F));

        }
        else if(level == 4){
            diskData.level = 4;
            diskData.mass = 4.0F + Random.Range(-1F, 1F) * 2.4F;
            diskData.score = 1000;
            diskData.speed = new Vector3(Random.Range(-10F, 10F), Random.Range(-10F, 10F), Random.Range(-10F, 10F));
            diskData.force = new Vector3(Random.Range(-10F, 10F), Random.Range(-10F, 10F), Random.Range(-10F, 10F));

        } 
        else if(level >= 5){
            diskData.level = 5;
            diskData.mass = 5.0F + Random.Range(-1F, 1F) * 4.0F;
            diskData.score = 5000;
            diskData.speed = new Vector3(Random.Range(-20F, 20F), Random.Range(-20F, 20F), Random.Range(-20F, 20F));
            diskData.force = new Vector3(Random.Range(-20F, 20F), Random.Range(-20F, 20F), Random.Range(-20F, 20F));
        }
    }

    void Update()
    {
        
    }
}
