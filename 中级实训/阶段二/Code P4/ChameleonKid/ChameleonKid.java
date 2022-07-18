/*
 * Create a class called ChameleonKid 
 * that extends ChameleonCritter as modified in exercise 1. 
 * A ChameleonKid changes its color 
 * to the color of one of the actors immediately in front or behind. 
 * If there is no actor in either of these locations, 
 * then the ChameleonKid darkens like the modified ChameleonCritter.
 */

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.util.ArrayList;

public class ChameleonKid extends ChameleonCritter{
    
    /**
     * overload getActors from Critter,
     * refer to getActors in CrabCritter
     * @return a set of actors that chameleonkid will copy their color
     */
    public ArrayList<Actor> getActors()
    {
        ArrayList<Actor> actors = new ArrayList<Actor>();
        int[] dirs = { Location.AHEAD, Location.HALF_CIRCLE };
        for (Location loc : getLocationsInDirections(dirs)){
            Actor actor = getGrid().get(loc);
            if (actor != null){
                actors.add(actor);
            }
        }
        return actors;
    }

    /**
     * Get valid neighbor locations in the given directions,
     * refer to getLocationsInDirections in CrabCritter
     * @param directions - an array of directions
     * @return a set of valid neighbor locations in the given directions
     */
    public ArrayList<Location> getLocationsInDirections(int[] directions)
    {
        ArrayList<Location> locs = new ArrayList<Location>();
        Grid gr = getGrid();
        Location loc = getLocation();
    
        for (int dir : directions){
            Location neighborLoc = loc.getAdjacentLocation(getDirection() + dir);
            if (gr.isValid(neighborLoc)){
                locs.add(neighborLoc);
            }
        }
        return locs;
    }  

}
