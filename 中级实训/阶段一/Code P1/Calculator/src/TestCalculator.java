import org.junit.Test;
import org.junit.Ignore;
import static org.junit.Assert.*;

public class TestCalculator {
  
	Calculator calculator = new Calculator();
	double a;
	double b;

	public TestCalculator(){
		a = 1234.56;
		b = 0;
	}

	@Test
	public void testAdd() { 
		System.out.println("Test Add");
	  	assertEquals("1234.56", calculator.cal_add(a, b));
	}

	@Test
	public void testSub() { 
		System.out.println("Test Sub");
	  	assertEquals("1234.56", calculator.cal_sub(a, b));
	}

	@Test
	public void testMul() { 
		System.out.println("Test Mul");
	  	assertEquals("0.0", calculator.cal_mul(a, b));
	}

	@Test
	public void testDev() { 
		System.out.println("Test Dev");
	  	assertEquals("ERR", calculator.cal_dev(a, b));
	}
}
