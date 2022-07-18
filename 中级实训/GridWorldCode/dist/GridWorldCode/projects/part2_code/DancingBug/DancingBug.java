import info.gridworld.actor.Bug;
import java.util.Arrays;

public class DancingBug extends Bug
{
    private int[] dancingTurns;
    private int turnIdx;

    /**
     * Constructs a dancing bug
     * @param turns the dancing turns array
     */
    public DancingBug(int[] turns)
    {
        turnIdx = 0;
        dancingTurns = Arrays.copyOf(turns, turns.length);
    }


    /**
     * Moves to the next location of the square.
     */
    public void act()
    {
    	// get turnTimes and update turnIdx
        if(turnIdx == dancingTurns.length){
            turnIdx = 0;
        }
        int turns = dancingTurns[turnIdx];
        turnIdx++;
        
        for(int i = 0; i < turns; i++){
            turn();
        }

	// try to move a bug each act
        if(canMove()){
            move();
        }
    }
}
