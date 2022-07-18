import info.gridworld.grid.*;
import info.gridworld.actor.*;

public class SparseBoundedGridRunner {
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        world.addGridClass("SparseBoundedGrid");
        world.add(new Location(2, 2), new Bug());
        world.show();
    }
}
