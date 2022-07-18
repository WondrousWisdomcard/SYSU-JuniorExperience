using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

// 游戏场景控制器，需要手动挂载到一个空对象上
public class FirstController : MonoBehaviour, IUserAction, ISceneController
{
    public GemFactory gemFactory;
    public GhostFactory ghostFactory;
    public PlayerFactory playerFactory;
    public GhostActionManager ghostActionManager;
    public GameEventManager gameEventManager;
    public RoomSensor roomSensor;
    public ScoreRecorder scoreRecorder;
    public UserGUI userGUI; 

    public List<GameObject> gems; 
    public List<GameObject> ghosts;
    public GameObject player;

    int restGemNum;
    int gameState;
    int countTime;
    int second;

    void Start(){
        
        // 设置FPS，用于确保秒数计时准确
        Application.targetFrameRate = 60;
        countTime = 0;
        second = 0;

        SSDirector.GetInstance().CurrentSceneController = this;

        gameObject.AddComponent<GemFactory>();
        gemFactory = Singleton<GemFactory>.Instance;

        gameObject.AddComponent<GhostFactory>();
        ghostFactory = Singleton<GhostFactory>.Instance;

        gameObject.AddComponent<PlayerFactory>();
        playerFactory = Singleton<PlayerFactory>.Instance;

        LoadResources();

        gameObject.AddComponent<GhostActionManager>();
        ghostActionManager = Singleton<GhostActionManager>.Instance;

        for(int i = 0; i < ghosts.Count; i++) {
            ghostActionManager.Walk(player, ghosts[i]);
        }

        gameObject.AddComponent<GameEventManager>();
        gameEventManager = Singleton<GameEventManager>.Instance;

        gameObject.AddComponent<RoomSensor>();
        roomSensor = Singleton<RoomSensor>.Instance;

        gameObject.AddComponent<ScoreRecorder>();
        scoreRecorder = Singleton<ScoreRecorder>.Instance;

        gameObject.AddComponent<UserGUI>();
        userGUI = Singleton<UserGUI>.Instance;

        Camera.main.GetComponent<CameraController>().player = player;

        restGemNum = gems.Count;
    }

    void Update() {
        // 计时
        if(userGUI.start == true && userGUI.gameover != true && userGUI.win != true){
            countTime += 1;
            if(countTime == 60){
                countTime = 0;
                second++;   
            }
        } 
        
        // UI更新
        userGUI.UpdateScoreText(scoreRecorder.score, restGemNum, second);
    }

    void OnEnable() {
        GameEventManager.OnGoalLost += OnGoalLost;
        GameEventManager.OnFollowing += OnFollowing;
        GameEventManager.GameOver += GameOver;
        GameEventManager.Win += Win;
        GameEventManager.OnGettingGem += OnGettingGem;
    }

    void OnDisable() {
        GameEventManager.OnGoalLost -= OnGoalLost;
        GameEventManager.OnFollowing -= OnFollowing;
        GameEventManager.GameOver -= GameOver;
        GameEventManager.Win -= Win;
        GameEventManager.OnGettingGem -= OnGettingGem;
    }

    // 在地图中随机生成十个宝石，随机分布在16个房间中
    public List<GameObject> generateRandomGems(){
        List<GameObject> gems = new List<GameObject>();

        int[] validRoom = new int[13] {1,2,3,4,5,6,8,9,10,11,12,13,16};
        int[] gemRoom = new int[10];
        int[] notChoose = new int[3];

        // 一共要生成10个宝石，设定上有13个房间（validRoom）可以放宝石
        // 随机选取其中3个房间（notChoose）不放宝石，剩下的10个房间（gemRoom）放宝石
        notChoose[0] = Random.Range(0, validRoom.Length);
        do{
            notChoose[1] = Random.Range(0, validRoom.Length);
        }while (notChoose[0] == notChoose[1]);
        do{
            notChoose[2] = Random.Range(0, validRoom.Length);
        }while (notChoose[0] == notChoose[2] || notChoose[1] == notChoose[2]);

        int j = 0;
        for(int i = 0; i < validRoom.Length; i++){
            if(i != notChoose[0] && i != notChoose[1] && i != notChoose[2]){
                int t = validRoom[i];
                gemRoom[j] = t;
                j++;
            }
        }

        // 调用宝石工厂创建10个宝石
        for(int i = 0; i < 10; i++){
            GameObject gem = gemFactory.GenGem(i + 1, gemRoom[i]);
            gems.Add(gem);
        }

        return gems;
    }

    // 在地图中生成若干幽灵，幽灵的个数和位置可以在此函数调整
    public List<GameObject> generateRandomGhosts(){
        
        List<GameObject> ghosts = new List<GameObject>();
    
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                if(i == 2 && j == 1){
                    // 起始房间：不生成灵魂
                }
                else if(i == 0 && j == 1){
                    // 邪恶房间：5只幽灵
                    GameObject ghost = ghostFactory.GenGhost(i, j, 2, 2);
                    ghosts.Add(ghost);

                    GameObject ghost2 = ghostFactory.GenGhost(i, j, -3, -2);
                    ghosts.Add(ghost2);

                    GameObject ghost3 = ghostFactory.GenGhost(i, j, 1, -3);
                    ghosts.Add(ghost3);

                    GameObject ghost4 = ghostFactory.GenGhost(i, j, -1, 2);
                    ghosts.Add(ghost4);

                    GameObject ghost5 = ghostFactory.GenGhost(i, j, -2, 1);
                    ghosts.Add(ghost5);
                }
                else{
                    // 普通房间：3只幽灵
                    GameObject ghost = ghostFactory.GenGhost(i, j, 2, 2);
                    ghosts.Add(ghost);

                    GameObject ghost2 = ghostFactory.GenGhost(i, j, -3, -2);
                    ghosts.Add(ghost2);

                    GameObject ghost3 = ghostFactory.GenGhost(i, j, 1, -3);
                    ghosts.Add(ghost3);
                }
            }
        }
        return ghosts;
    }
    
    // 载入资源：生成玩家、幽灵和宝石
    public void LoadResources(){
        Debug.Log("Load Resource...");

        gems = generateRandomGems();
        ghosts = generateRandomGhosts();
        player = playerFactory.GenPlayer();
    }

    // 使用 Scene Manager 重新载入游戏场景
    // 参考博客：https://www.cnblogs.com/caicaicaicai/p/6475600.html 来解决不渲染光线的问题
    public void Restart(){
        SceneManager.LoadScene("Scenes/Play");
    }

    // 每甩开一个幽灵，玩家得 1 分
    public void OnGoalLost(GameObject ghost) {
        ghostActionManager.Walk(player, ghost);
        if(player.GetComponent<PlayerData>().alive){
            scoreRecorder.Record(1);
        }
    }

    // 玩家进入幽灵的视野，幽灵开始追击
    public void OnFollowing(GameObject ghost) {
        if(player.GetComponent<PlayerData>().alive) {
            ghostActionManager.Follow(player, ghost);
            Debug.Log("I See U!");
        }
    }

    // 玩家获取水晶，当获得全部水晶，游戏获胜
    public void OnGettingGem(GameObject gem) {
        gem.SetActive(false);
        restGemNum--;
        if(restGemNum == 0) {
            Win();
        }
    }

    // 失败
    public void GameOver() {
        Debug.Log("GameOver");
        player.GetComponent<PlayerData>().alive = false;
        player.SetActive(false);
        userGUI.gameover = true;
    }

    // 胜利，幽灵消失，你可以在房间里闲逛
    public void Win() {
        Debug.Log("YouWin");
        for(int i = 0; i < ghosts.Count; i++){
            ghosts[i].SetActive(false);
        }
        userGUI.win = true;
    }

}
