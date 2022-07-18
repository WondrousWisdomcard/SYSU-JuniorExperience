import info.gridworld.grid.*;

import java.util.ArrayList;

/**
 * Suppose that a program requires a very large bounded grid that contains very
 * few objects and that the program frequently calls the getOccupiedLocations
 * method (as, for example, ActorWorld). Create a class SparseBoundedGrid that
 * uses a “sparse array” implementation. Your solution need not be a generic
 * class; you may simply store occupants of type Object. The “sparse array” is
 * an array list of linked lists. Each linked list entry holds both a grid
 * occupant and a column index. Each entry in the array list is a linked list or
 * is null if that row is empty.
 */
public class SparseBoundedGrid<E> extends AbstractGrid<E> {

    private SparseGridNode[] occupantArray;

    private int rows;
    private int cols;

    /**
     * Constructs an empty bounded grid with the given dimensions
     * 
     * @param rows number of rows in SparseBoundedGrid
     * @param cols number of columns in SparseBoundedGrid
     */
    public SparseBoundedGrid(int rows, int cols) {
        if (cols <= 0 || rows <= 0)
            throw new IllegalArgumentException("cols/rows must be greater than 0");

        this.cols = cols;
        this.rows = rows;
        occupantArray = new SparseGridNode[rows];
    }

    public int getNumRows() {
        return rows;
    }

    public int getNumCols() {
        return cols;
    }

    public boolean isValid(Location loc) {
        return 0 <= loc.getRow() && loc.getRow() < getNumRows() && 0 <= loc.getCol() && loc.getCol() < getNumCols();
    }

    public ArrayList<Location> getOccupiedLocations() {

        ArrayList<Location> locations = new ArrayList<Location>();

        for (int i = 0; i < rows; i++) {
            SparseGridNode nodePtr = occupantArray[i];
            while (nodePtr != null) {
                locations.add(new Location(i, nodePtr.getCol()));
                nodePtr = nodePtr.getNext();
            }
        }

        return locations;
    }

    public E get(Location loc) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));

        SparseGridNode nodePtr = occupantArray[loc.getRow()];
        while (nodePtr != null) {
            if (nodePtr.getCol() == loc.getCol()) {
                return (E)nodePtr.getOccupant();
            }
            nodePtr = nodePtr.getNext();
        }
        return null;
    }

    public E put(Location loc, E obj) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));

        if (obj == null)
            throw new NullPointerException("obj == null");

        E oldOccupant = remove(loc);

        SparseGridNode headPtr = occupantArray[loc.getRow()];
        occupantArray[loc.getRow()] = new SparseGridNode(obj, loc.getCol(), headPtr);

        return oldOccupant;
    }

    public E remove(Location loc) {
        if (!isValid(loc))
            throw new IllegalArgumentException(getNotValidMessage(loc));

        SparseGridNode headPtr = occupantArray[loc.getRow()];

        // null head situation
        if(headPtr == null){
            return null;
        }

        if(headPtr.getCol() == loc.getCol()){
            // head situation
            occupantArray[loc.getRow()] = headPtr.getNext();
            return (E)headPtr.getOccupant();
        }
        else{
            // other situations
            SparseGridNode prePtr = headPtr;
            while(prePtr.getNext() != null){
                SparseGridNode tempPtr = prePtr.getNext();
                if(tempPtr.getCol() == loc.getCol()){
                    prePtr.setNext(tempPtr.getNext());
                    return (E)tempPtr.getOccupant();
                }
                else{
                    prePtr = tempPtr;
                }
            }
            return null;
        }

    }
    
    public String getNotValidMessage(Location loc){
    	return "Location " + loc + " is not valid";
    }

}
