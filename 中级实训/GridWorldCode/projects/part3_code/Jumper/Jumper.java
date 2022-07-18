import info.gridworld.actor.*;
import info.gridworld.grid.*;
import java.awt.Color;


/**
 * A Jumper is an actor that can jump and turn.
 */
public class Jumper extends Actor
{
    /**
     * Constructs a blue jumper.
     */
    public Jumper()
    {
        setColor(Color.BLUE);
    }

    /**
     * Constructs a jumper of a given color.
     * @param jumperColor the color for this jumper
     */
    public Jumper(Color jumperColor)
    {
        setColor(jumperColor);
    }

    /**
     * Jumps ifit can jump, turns otherwise.
     */
    public void act()
    {
        if(canJump())
            jump();
        else
            turn();
    }

    /**
     * Turns the bug 45 degrees to the right without changing its location.
     */
    public void turn()
    {
        setDirection(getDirection() + Location.HALF_RIGHT);
    }

    /**
     * Jumps the jump forward
     */
    public void jump()
    {
        Grid<Actor> grid = getGrid();
        if(grid == null){
            return;
        }
        Location loc = getLocation();
        Location next = loc.getAdjacentLocation(getDirection());
        if(grid.isValid(next)){
            Location dest = next.getAdjacentLocation(getDirection());
            if(grid.isValid(dest)){
                moveTo(dest);
            }
            else{
                removeSelfFromGrid();
            }
        }
    }

    /**
     * Tests whether this jumper can jump forward into a location that is empty or
     * contains a flower.
     * @return true if this jumper can move.
     */
    public boolean canJump()
    {
        Grid<Actor> gr = getGrid();
        if(gr == null){
            return false;
        }

        Location loc = getLocation();
        Location next = loc.getAdjacentLocation(getDirection());
        if(!gr.isValid(next)){
            return false;
        }
        else{
            Location dest = next.getAdjacentLocation(getDirection());
            if(gr.isValid(dest)){
                Actor neighbor = gr.get(dest);
                return (neighbor == null) || (neighbor instanceof Flower);
                // ok to move into empty location or onto flower
                // not ok to move onto any other actor
            }
            else{
                return false;
            }
        }
    }
}
