import info.gridworld.actor.*;
import info.gridworld.grid.*;

public class ZBug extends Bug
{
    private int steps;
    private int sideLength;
    private int turns;

    /**
     * Constructs a Z bug that traces a square of a given side length
     * @param length the side length
     */
    public ZBug(int length)
    {
        steps = 0;
        turns = 0;
        sideLength = length;
        setDirection(Location.EAST);
    }

    /**
     * Moves to the next location of the square.
     */
    public void act()
    {
        if(canMove() == false || turns > 2){
            // do nothing
        }
        else if (steps < sideLength)
        {
            move();
            steps++;
        }
        else if (steps == sideLength)
        {
            turns++;
            // turn0: bug move to east
            // turn1: bug move to sounthwest
            // turn2: bug move to east again
            if(turns == 1){
                setDirection(Location.SOUTHWEST);
                steps = 0;
            }
            else if(turns == 2){
                setDirection(Location.EAST);
                steps = 0;
            }
        }
    }
}
