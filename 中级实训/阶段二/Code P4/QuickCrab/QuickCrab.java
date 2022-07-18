/**
 * Create a class QuickCrab that extends CrabCritter. 
 * A QuickCrab processes actors the same way a CrabCritter does. 
 * A QuickCrab moves to one of the two locations, randomly selected, 
 * that are two spaces to its right or left, 
 * if that location and the intervening location are both empty. 
 * Otherwise, a QuickCrab moves like a CrabCritter.
 */

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;
import java.util.ArrayList;

public class QuickCrab extends CrabCritter{

    public QuickCrab()
    {
        setColor(Color.YELLOW);
    }

    /**
     * overload getMoveLocations of CrabCritter
     * @return list of empty locations immediately to the right and to the left
     */
    public ArrayList<Location> getMoveLocations()
    {
        ArrayList<Location> locs = new ArrayList<Location>();
        Grid grid = getGrid();

        int dirLeft = getDirection() + Location.LEFT;
        int dirRight = getDirection() + Location.RIGHT;

        Location locLeft = getLocation().getAdjacentLocation(dirLeft);
        if(grid.isValid(locLeft) && grid.get(locLeft) == null) {
            locs.add(locLeft);
            Location locLeftLeft = locLeft.getAdjacentLocation(dirLeft);
            if(grid.isValid(locLeftLeft) && grid.get(locLeftLeft) == null) {
                locs.add(locLeftLeft);
            }
        }

        Location locRight = getLocation().getAdjacentLocation(dirRight);
        if(grid.isValid(locRight) && grid.get(locRight) == null) {
            locs.add(locRight);
            Location locRightRight = locRight.getAdjacentLocation(dirRight);
            if(grid.isValid(locRightRight) && grid.get(locRightRight) == null) {
                locs.add(locRightRight);
            }
        }              

        return locs;
    }
}
