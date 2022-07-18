import info.gridworld.actor.ActorWorld;
import info.gridworld.grid.Location;

import java.awt.Color;

/**
 * This class runs a world that contains Dancing bugs.
 */
public class DancingBugRunner
{
    public static void main(String[] args)
    {
        //int[] turns = {9,3,5,8,9};
        int[] turns = {1,2,3,4,5,6,7,8};
        ActorWorld world = new ActorWorld();
        
        // Alice: Orange DancingBug
        DancingBug alice = new DancingBug(turns);
        alice.setColor(Color.ORANGE);
        world.add(new Location(7, 8), alice);

		// Bob: Green DancingBug
        DancingBug bob = new DancingBug(turns);
        bob.setColor(Color.GREEN);
        world.add(new Location(1, 1), bob);

        world.show();
    }
}
