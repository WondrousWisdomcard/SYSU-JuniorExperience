using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FirstController : MonoBehaviour, ISceneController, IUserAction
{
    public UserGUI userGUI;
    public DiskFactory diskFactory;
    public RoundController roundController;
    public ScoreRecorder scoreRecorder;

    void Start(){
        SSDirector.GetInstance().currentSceneController = this;
        LoadResources();
    }

    void Update(){
    }

    public void LoadResources(){
        Debug.Log("Load Resource...");

        gameObject.AddComponent<UserGUI>();
        userGUI = Singleton<UserGUI>.Instance;

        gameObject.AddComponent<DiskFactory>();
        diskFactory = Singleton<DiskFactory>.Instance;

        gameObject.AddComponent<RoundController>();
        roundController = Singleton<RoundController>.Instance;

        gameObject.AddComponent<ScoreRecorder>();
        scoreRecorder = Singleton<ScoreRecorder>.Instance;
        
        gameObject.AddComponent<CCActionManager>();
        gameObject.AddComponent<PhysisActionManager>();
    }

    public void Restart(){
        userGUI.Reset();
        roundController.Reset();
    }

    public void Hit(Vector3 position){
        Camera camera = Camera.main;
        Ray ray = camera.ScreenPointToRay(position);

        RaycastHit[] hits = Physics.RaycastAll(ray);

        foreach(RaycastHit hit in hits){
            if(hit.collider.gameObject.GetComponent<DiskData>() == null){
                continue;
            }
            GameObject disk = hit.collider.gameObject;
            roundController.UpdateScore(disk.GetComponent<DiskData>());
            diskFactory.FreeDisk(disk);
        }

        userGUI.UpdateScoreText(roundController.GetRound(), roundController.scoreRecorder.GetScore());
    }

    public void GameStart(){
        roundController.GameStart();
    }

}
