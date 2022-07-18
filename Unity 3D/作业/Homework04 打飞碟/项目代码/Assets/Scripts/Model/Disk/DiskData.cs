using System;
using UnityEngine;

[System.Serializable]
public class DiskData : MonoBehaviour
{
    [Tooltip("飞碟级别")]
    public int level;
    [Tooltip("飞碟质量")]
    public float mass;
    [Tooltip("飞碟颜色")]
    public Color color;
    [Tooltip("击中分数")]
    public int score;
    [Tooltip("初始速度")]
    public Vector3 speed;
    [Tooltip("恒定外力")]
    public Vector3 force;    
}

[CreateAssetMenu(fileName = "DiskItem", menuName = "(ScriptableObject)DiskItem")]
public class DiskItem : ScriptableObject
{
    public string Name;
    [Tooltip("飞碟属性")]
    public DiskData diskData;
}