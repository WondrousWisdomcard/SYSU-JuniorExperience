import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

public class RockHoundRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();

        // Create 8 random rocks
        world.add(new Location(7, 8), new Rock());
        world.add(new Location(3, 3), new Rock());
        world.add(new Location(0, 2), new Rock());
        world.add(new Location(2, 8), new Rock());
        world.add(new Location(5, 5), new Rock());
        world.add(new Location(1, 5), new Rock());
        world.add(new Location(7, 2), new Rock());
        world.add(new Location(5, 1), new Rock());

        // Create 2 random bugs that RockHound will not eat
        world.add(new Location(3, 4), new Bug(Color.BLUE));
        world.add(new Location(2, 3), new Bug(Color.GREEN));

        // Create 2 RockHound
        world.add(new Location(4, 4), new RockHound());
        world.add(new Location(8, 5), new RockHound());

        world.show();
    }
}
