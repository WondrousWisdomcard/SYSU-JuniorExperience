import info.gridworld.grid.*;

/**
 * SparseGridNode is the basic structure of ArrayList in SparseBoundedGrid  
 */ 
public class SparseGridNode{

    private Object occupant;
    private int col;
    private SparseGridNode next;

    /**
     * Constructor 
     * @param occupant the actor
     * @param col the column number in grid
     * @param next the pointer to next occupied grid node
     */
    public SparseGridNode(Object occupant, int col, SparseGridNode next){
        this.occupant = occupant;
        this.col = col;
        this.next = next;
    }

    public Object getOccupant(){
        return occupant;
    }

    public void setOccupant(Object occupant){
        this.occupant = occupant;
    }

    public int getCol(){
        return col;
    }

    public void setCol(int col){
        this.col = col;
    }

    public SparseGridNode getNext(){
        return next;
    }

    public void setNext(SparseGridNode next){
        this.next = next;
    }

}