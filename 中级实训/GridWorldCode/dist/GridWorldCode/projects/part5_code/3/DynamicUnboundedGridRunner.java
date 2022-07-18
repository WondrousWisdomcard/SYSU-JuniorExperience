import info.gridworld.grid.*;
import info.gridworld.actor.*;

public class DynamicUnboundedGridRunner {
    public static void main(String[] args)
    {
    	DynamicUnboundedGrid<Actor> grid = new DynamicUnboundedGrid<Actor>();
        ActorWorld world = new ActorWorld(grid);
        world.addGridClass("DynamicUnboundedGrid");
        world.add(new Location(18, 2), new Bug());
        world.show();
    }
}
