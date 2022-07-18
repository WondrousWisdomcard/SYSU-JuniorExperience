import org.junit.Test;
import org.junit.Ignore;
import static org.junit.Assert.assertEquals;

public class TestHelloWorld {
  
   HelloWorld helloworld = new HelloWorld();

   @Test
   public void testGetString() { 
      System.out.println("Inside testGetString()");     
      assertEquals("HelloWorld", HelloWorld.getString());
   }

}
