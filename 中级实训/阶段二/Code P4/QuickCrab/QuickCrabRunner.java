import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

public class QuickCrabRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();

        // Create 3 random rocks
        world.add(new Location(7, 8), new Rock());
        world.add(new Location(3, 3), new Rock());
        world.add(new Location(0, 2), new Rock());

        // Create 4 random flowers with different colors
        world.add(new Location(2, 8), new Flower(Color.BLUE));
        world.add(new Location(5, 5), new Flower(Color.PINK));
        world.add(new Location(1, 5), new Flower(Color.RED));
        world.add(new Location(7, 2), new Flower(Color.YELLOW));

        // Create 1 random bug that drops flower
        world.add(new Location(5, 1), new Bug(Color.PINK));

        // Create 2 QuickCrabs
        world.add(new Location(4, 4), new QuickCrab());
        world.add(new Location(8, 5), new QuickCrab());

        world.show();
    }
}