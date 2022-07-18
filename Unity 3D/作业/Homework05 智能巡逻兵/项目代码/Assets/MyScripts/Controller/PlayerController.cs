using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 玩家控制器：指定玩家操作
public class PlayerController : MonoBehaviour
{
    private Animator ani;

    void Start()
    {
        ani = GetComponent<Animator>();
    }

    // W键前进，Q E A D S 转向，空格键停下
    void Update()
    {
        if(Input.GetKeyDown("w")){
            ani.SetBool("WalkBool", true);
        }
        else if(Input.GetKeyDown("q")){
            transform.Rotate(0, -45F, 0);
        }
        else if(Input.GetKeyDown("e")){
            transform.Rotate(0, 45F, 0);
        }
        else if(Input.GetKeyDown("a")){
            transform.Rotate(0, -90F, 0);
        }
        else if(Input.GetKeyDown("s")){
            transform.Rotate(0, 180F, 0);
        }
        else if(Input.GetKeyDown("d")){
            transform.Rotate(0, 90F, 0);
        }

        if(Input.GetKey(KeyCode.Space)){
            ani.SetBool("WalkBool", false);
        }
    }
}
