import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

/**
 * This class runs a world that contains spiral bugs.
 */
public class SpiralBugRunner
{
    public static void main(String[] args)
    {
        Grid<Actor> grid = new UnboundedGrid<Actor>();
        ActorWorld world = new ActorWorld(grid);
        SpiralBug alice = new SpiralBug(2);
        alice.setColor(Color.ORANGE);
        world.add(new Location(2, 2), alice);
        world.show();
    }
}
