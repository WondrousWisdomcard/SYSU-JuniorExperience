import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

public class ModifiedChameleonCritterRunner
{

    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();
        
        // Create a flower
        world.add(new Location(1, 0), new Flower(Color.ORANGE));

        // Create a ModifiedChameleonCritter
        // A ModifiedChameleonCritter changes its color to the color
        // of one of the actors immediately in front or behind. 
        world.add(new Location(0, 0), new ModifiedChameleonCritter());

        world.show();
    }
}
