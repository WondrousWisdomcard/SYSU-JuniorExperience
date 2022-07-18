import org.junit.Test;
import org.junit.Ignore;
import static org.junit.Assert.assertEquals;

import info.gridworld.actor.*;
import info.gridworld.grid.*;
import java.awt.Color;

public class JumperTest {

    ActorWorld world;
    Jumper jumper;
    Rock rock;
    Flower flower;
    
    public JumperTest(){
        world = new ActorWorld();
        jumper = new Jumper();
        rock = new Rock();
        flower = new Flower();
        world.add(new Location(1, 1), jumper);
        world.add(new Location(1, 3), rock);
        world.add(new Location(1, 2), flower);
    }
    

    // 测试Jumper(3,3)是否能跳到一个Rock(3,5)上，答案是NO
    @Test
    public void testCanJumpRock() {
        jumper.moveTo(new Location(3,3));
        jumper.setDirection(Location.EAST);
        rock.moveTo(new Location(3,5));
        assertEquals(false, jumper.canJump());
    }
    
    // 测试Jumper(4,3)是否能跳到一个Flower(4,5)上，答案是YES
    @Test
    public void testCanJumpFlower() {
        jumper.moveTo(new Location(4,3));
        jumper.setDirection(Location.EAST);
        flower.moveTo(new Location(4,5));
        assertEquals(true, jumper.canJump());
    }

    @Test
    public void testCanJumpEdge() {
        jumper.moveTo(new Location(9,9));
        jumper.setDirection(Location.SOUTH);
        assertEquals(false, jumper.canJump());
    }

    @Test
    public void testCanJumpOverRock() {
        jumper.moveTo(new Location(4,2));
        jumper.setDirection(Location.EAST);
        rock.moveTo(new Location(4,3));
        assertEquals(true, jumper.canJump());
    }

    @Test
    public void testNormalJump() {
        jumper.moveTo(new Location(5,1));
        jumper.setDirection(Location.SOUTHEAST);
        jumper.act();
        assertEquals(jumper.getLocation().getRow(), 7);
        assertEquals(jumper.getLocation().getCol(), 3);
    }

}
