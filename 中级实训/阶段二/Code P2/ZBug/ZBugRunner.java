import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

/**
 * This class runs a world that contains Z bugs.
 */
public class ZBugRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        
        // Alice: Orange ZBug that can finsih its job
        ZBug alice = new ZBug(5);
        alice.setColor(Color.ORANGE);
        world.add(new Location(1, 1), alice);

	// Bob: Blue ZBug that can't finish its job for narrow space
        ZBug bob = new ZBug(5);
        bob.setColor(Color.BLUE);
        world.add(new Location(8, 8), bob);
        
        world.show();
    }
}
