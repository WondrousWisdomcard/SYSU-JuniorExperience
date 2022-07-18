/**
 * Create a class KingCrab that extends CrabCritter. 
 * A KingCrab gets the actors to be processed in the same way a CrabCritter does. 
 * A KingCrab causes each actor that it processes to move one location further away from the KingCrab. 
 * If the actor cannot move away, the KingCrab removes it from the grid. 
 * When the KingCrab has completed processing the actors, it moves like a CrabCritter.
 */

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;
import java.util.ArrayList;

public class KingCrab extends CrabCritter{

    public KingCrab(){
        setColor(Color.BLACK);
    }
    
    /**
     * A KingCrab causes each actor that it processes to move one location further away from the KingCrab. 
     * If the actor cannot move away, the KingCrab removes it from the grid. 
     * @param actors the actors to be processed
     */
    public void processActors(ArrayList<Actor> actors)
    {
        for (Actor actor : actors)
        {
            Grid grid = getGrid();
            Location aLoc = actor.getLocation();
            ArrayList<Location> locs = grid.getEmptyAdjacentLocations(aLoc);
            for(Location loc : locs){
                if(isSaveLocation(loc)){
                    actor.moveTo(loc);
                    break;
                }
            }
            if(actor.getLocation().equals(aLoc)){
                actor.removeSelfFromGrid();
            }
        }
    }

    /**
     * To judge whether a location is safe for kingCrab
     * @param otherActorLocation the location of actor
     * @return true if the location is safe, which means the distance 
     * between kingCrab and actor is greater than 1.0
     */
    private boolean isSaveLocation(Location otherActorLocation){
        double distance = 0;
        Location kingCrabLocation = getLocation();
        double deltaRow = kingCrabLocation.getRow() - otherActorLocation.getRow();
        double deltaCol = kingCrabLocation.getCol() - otherActorLocation.getCol(); 
        distance = Math.sqrt(deltaRow * deltaRow + deltaCol * deltaCol);
        return distance > 1.0;
    }
}
