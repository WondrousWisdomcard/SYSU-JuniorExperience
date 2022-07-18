using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FirstController : MonoBehaviour, IUserAction
{
    public HealthBar healthBar;
    public HealthBar2 healthBar2;

    public float hurt = 250F;
    public float heal = 1000F;

    void Start() {
        gameObject.AddComponent<HealthBar>();
        healthBar = Singleton<HealthBar>.Instance;
    }

    void Update() {

        if(Input.GetKeyDown("f")){
            Hurt();
        }

        if(Input.GetKeyDown("h")){
            Heal();
        }

        if(Input.GetKeyDown("r")){
            Restart();
        }

    }

    public void Hurt() {
        healthBar.Hurt(hurt);
        healthBar2.Hurt(hurt);
    }

    public void Heal() {
        healthBar.Heal(heal);
        healthBar2.Heal(heal);
    }

    public void Restart() {
        healthBar.restart = true;
        healthBar2.restart = true;
    }
}
