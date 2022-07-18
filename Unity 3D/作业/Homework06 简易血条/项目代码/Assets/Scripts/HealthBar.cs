using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HealthBar : MonoBehaviour
{

    public float healthUpperLimit;
    private float healthValue;

    public bool restart;

    void Start() {
        healthUpperLimit = 4000.0F;
        healthValue = healthUpperLimit;
        restart = false;
    }

    void Update() {
        if(restart){
            healthUpperLimit = 4000.0F;
            healthValue = healthUpperLimit;
            restart = false;
        }
    }

    public void Hurt(float h) {
        healthValue -= h;
        if(healthValue <= 0){
            healthValue = 0;
        }
    }

    public void Heal(float h) {
        if(healthValue > 0){
            healthValue += h;
            if(healthValue >= healthUpperLimit) {
                healthValue = healthUpperLimit;
            }
        }
    }

    void OnGUI() {

        GUIStyle healthTextStyle = new GUIStyle();
        healthTextStyle.fontSize = 20;
        healthTextStyle.alignment = TextAnchor.MiddleCenter;
        
        if(healthValue < healthUpperLimit * 0.3) {
            GUI.color = Color.red;
        }
        else if(healthValue < healthUpperLimit * 0.6) {
            GUI.color = Color.yellow;
        }
        else {
            GUI.color = Color.green;
        }
        
        GUI.HorizontalScrollbar(new Rect(30, 30, Screen.width - 60, 30), 0.0F, healthValue, 0.0F, healthUpperLimit);
        GUI.Label(new Rect(30, 50, Screen.width - 60, 20), healthValue.ToString() + " / " + healthUpperLimit.ToString(), healthTextStyle);
        
    }

}
