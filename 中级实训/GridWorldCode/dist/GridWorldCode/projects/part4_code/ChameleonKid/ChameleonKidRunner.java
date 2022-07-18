import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;

public class ChameleonKidRunner
{
    public static void main(String[] args)
    {
        ActorWorld world = new ActorWorld();

        // Create 3 random rocks
        world.add(new Location(7, 8), new Rock());
        world.add(new Location(3, 3), new Rock());
        world.add(new Location(0, 2), new Rock());

        // Create 8 random flowers with different colors
        world.add(new Location(2, 8), new Flower(Color.BLUE));
        world.add(new Location(5, 5), new Flower(Color.PINK));
        world.add(new Location(1, 5), new Flower(Color.RED));
        world.add(new Location(7, 2), new Flower(Color.YELLOW));
        world.add(new Location(2, 3), new Flower(Color.GREEN));
        world.add(new Location(5, 1), new Flower(Color.PINK));
        world.add(new Location(1, 0), new Flower(Color.ORANGE));
        world.add(new Location(3, 4), new Flower(Color.BLUE));

        // Create 3 ChameleonKids
        // A ChameleonKid changes its color to the color
        // of one of the actors immediately in front or behind. 
        world.add(new Location(4, 4), new ChameleonKid());
        world.add(new Location(8, 5), new ChameleonKid());
        world.add(new Location(0, 0), new ChameleonKid());

        world.show();
    }
}