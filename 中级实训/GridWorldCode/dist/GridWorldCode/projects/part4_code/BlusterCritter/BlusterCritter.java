/*
 * Create a class BlusterCritter that extends Critter. 
 * A BlusterCritter looks at all of the neighbors within **two steps of its current location**. 
 * For a BlusterCritter not near an edge, this includes 24 locations. 
 * It counts the number of critters in those locations. 
 * If there are fewer than c critters, the BlusterCritter’s color gets brighter (color values increase). 
 * If there are c or more critters, the BlusterCritter’s color darkens (color values decrease). 
 * Here, c is a value that indicates the courage of the critter. It should be set in the constructor.
 */

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.util.ArrayList;
import java.awt.Color;

public class BlusterCritter extends Critter{

    private static final Color DEFAULT_COLOR = new Color(150,0,0);
    private static final double DARKENING_FACTOR = 0.1;
    private int c = 10;

    /**
     * Constructor with param
     * @param c courage of the critter
     */
    public BlusterCritter(int c) {
        this.c = c;
        setColor(DEFAULT_COLOR);
    }


    /**
     * Overload getActor of Critter, A BlusterCritter looks at 
     * all of the neighbors within two steps of its current location. 
     * @return a list of critter's neighbors
     */
    public ArrayList<Actor> getActors()
    {
        int row = getLocation().getRow();
        int col = getLocation().getCol();
        
        ArrayList<Actor> actors = new ArrayList<Actor>();
        Grid grid = getGrid();

        for(int i = row - 2; i < row + 2; i++){
            for(int j = col - 2; j < col + 2; j++){
                Location loc = new Location(i, j);
                if(grid.isValid(loc)){
                    Actor actor = (Actor)grid.get(loc);
                    if(actor != null && actor != this){
                        actors.add(actor);
                    }
                }
            }
        }
        return actors;
    }
    
    /**
     * Overload processActors of Critter
     * If there are fewer than c critters, the BlusterCritter’s color gets brighter (color values increase). 
     * If there are c or more critters, the BlusterCritter’s color darkens (color values decrease). 
     * @param actors the actors to be processed
     */
    public void processActors(ArrayList<Actor> actors)
    {
        int n = actors.size();
        // System.out.println("" + n);
        Color color;
        int red;
        int green;
        int blue;
        if (n >= c){
        	// lighten
            color = getColor();
            red = (int) (color.getRed() * (1 - DARKENING_FACTOR));
            green = (int) (color.getGreen() * (1 - DARKENING_FACTOR));
            blue = (int) (color.getBlue() * (1 - DARKENING_FACTOR));
        }
        else{
            color = getColor();
            // darken
            red = (int) (color.getRed() * (1 + DARKENING_FACTOR));
            if(red > 255){
            	red = 255;
            }
            green = (int) (color.getGreen() * (1 + DARKENING_FACTOR));
            if(green > 255){
            	green = 255;
            }
            blue = (int) (color.getBlue() * (1 + DARKENING_FACTOR));
            if(blue > 255){
            	blue = 255;
            }
            
        }
        setColor(new Color(red, green, blue));
    }
}
