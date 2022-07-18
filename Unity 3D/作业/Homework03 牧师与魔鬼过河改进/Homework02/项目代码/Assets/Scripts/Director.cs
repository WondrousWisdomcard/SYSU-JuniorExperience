public class Director : System.Object
{
    // Singlton
    private static Director _instance;
    public ISceneController currentSceneController{ get; set; }

    public static Director getInstance(){
        if(_instance == null){
            _instance = new Director();
        }
        return _instance;
    }
}
