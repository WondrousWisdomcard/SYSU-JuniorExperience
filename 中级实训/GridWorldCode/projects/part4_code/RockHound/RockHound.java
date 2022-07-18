/*
 * Create a class called RockHound that extends Critter. 
 * A RockHound gets the actors to be processed in the same way as a Critter. 
 * It removes any rocks in that list from the grid. 
 * A RockHound moves like a Critter.
 */ 

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.util.ArrayList;

public class RockHound extends Critter{

    /** 
     * A RockRound only remove rock
     * @param actors the actors to be processed
     */
    public void processActors(ArrayList<Actor> actors){
        for (Actor a : actors){
            if (a instanceof Rock)
                a.removeSelfFromGrid();
        }
    }
}
