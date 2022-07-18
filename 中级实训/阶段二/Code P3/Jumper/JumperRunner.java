import info.gridworld.actor.*;
import info.gridworld.grid.*;
import java.awt.Color;

/**
 * This class runs a world that contains jumper. <br />
 * This class is not tested on the AP CS A and AB exams.
 */
public class JumperRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        Jumper jumper = new Jumper();
        Rock rock = new Rock();
        Flower flower = new Flower();

        world.add(new Location(1, 1), jumper);
        world.add(new Location(1, 3), rock);
        world.add(new Location(3, 3), flower);
        world.show();
    }
}
