import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.Location;

import java.awt.Color;

/**
 * This class runs a world that contains circle bugs.
 */
public class CircleBugRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        
        // Alice: Orange CircleBug that create 3 * 3 circle
        CircleBug alice = new CircleBug(2);
        alice.setColor(Color.ORANGE);
        
        // Bob: Red CircleBug that create 2 * 2 circle
        CircleBug bob = new CircleBug(1);
        world.add(new Location(7, 8), alice);
        world.add(new Location(5, 5), bob);
        world.show();
    }
}
