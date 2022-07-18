import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

public class KingCrabRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();

        // Create 2 random rocks
        world.add(new Location(4, 4), new Rock());
        world.add(new Location(6, 6), new Rock());

        // Create 14 random flowers with different colors
        world.add(new Location(5, 4), new Flower(Color.BLUE));
        world.add(new Location(5, 6), new Flower(Color.PINK));
        world.add(new Location(4, 5), new Flower(Color.RED));
        world.add(new Location(6, 5), new Flower(Color.YELLOW));
        for(int i = 0; i < 10; i++){
        	world.add(new Location(0, i), new Flower());
        }
        
        // Create 2 KingCrabs
        world.add(new Location(5, 5), new KingCrab());
        world.add(new Location(1, 5), new KingCrab());

        world.show();
    }
}
