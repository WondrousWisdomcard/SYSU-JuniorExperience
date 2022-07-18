import org.junit.Test;
import static org.junit.Assert.assertEquals;
import java.io.*;
import javax.imageio.ImageIO;
import java.awt.*;
import java.util.logging.*;

import java.awt.image.BufferedImage;
import imagereader.*;

/**
 * A Test File based on JUnit4
 * to check whether ImplementImageProcessor and ImplementImageIO
 * can satisfy the requirements.
 **/
public class ImageReaderTest {

	IImageIO imageioer;
    IImageProcessor processor;
    Image image1;
    Image image2;
    String filePath = "/home/max/Desktop/se-training/Stage3/ImageReader/bmptest/";
    String logtext = "log.text";
    
    public ImageReaderTest(){
    	imageioer = new ImplementImageIO();
        processor = new ImplementImageProcessor();
        
        Logger logger = Logger.getLogger(logtext);
        /**
         * In Constructor,
         * We create the .bmp file using our code and store them in bmptest/myresult
         * Next step we re going to using BufferedImage to check 
         * whether our images and goal images are equal.
         */
        try {
			image1 = imageioer.myRead(filePath + "1.bmp");
			image2 = imageioer.myRead(filePath + "2.bmp");
			
			imageioer.myWrite(processor.showChanelR(image1), filePath + "myresult/1_red.bmp");
			imageioer.myWrite(processor.showChanelG(image1), filePath + "myresult/1_green.bmp");
			imageioer.myWrite(processor.showChanelB(image1), filePath + "myresult/1_blue.bmp");
			imageioer.myWrite(processor.showGray(image1), filePath + "myresult/1_gray.bmp");
			
			imageioer.myWrite(processor.showChanelR(image2), filePath + "myresult/2_red.bmp");
			imageioer.myWrite(processor.showChanelG(image2), filePath + "myresult/2_green.bmp");
			imageioer.myWrite(processor.showChanelB(image2), filePath + "myresult/2_blue.bmp");
			imageioer.myWrite(processor.showGray(image2), filePath + "myresult/2_gray.bmp");

		} catch (IOException e) {
			logger.log(Level.WARNING, "imageReaderTest");
		}
    }
    
    /**
     * isEqual is to check whether two images are equal
     * by checking their width, height and corrsponding pixels
     * @return ture if two images are equal
     **/
    public boolean isEqual(BufferedImage image1, BufferedImage image2) {
    	int w1 = image1.getWidth(null);
        int h1 = image1.getHeight(null);
        
        int w2 = image2.getWidth(null);
        int h2 = image2.getHeight(null);
        
        if(w1 != w2 || h1 != h2) {
        	return false;
        }       
        
        for(int i = 0; i < w1; i++) {
        	for(int j = 0; j < h1; j++) {
        		if(image1.getRGB(i, j) != image2.getRGB(i, j)) {
        			return false;
        		}
        	}
        }
        
        return true;
    }

	/**
	 * Test of Chanel Red Image
	 */
    @Test
    public void testRed() {
    	Logger logger = Logger.getLogger(logtext);
    	try {
    		String goalFilePath1 = filePath + "goal/1_red_goal.bmp";
    		String goalFilePath2 = filePath + "goal/2_red_goal.bmp";
    		
    		BufferedImage redImage1Goal = ImageIO.read(new FileInputStream(goalFilePath1));
    		BufferedImage redImage2Goal = ImageIO.read(new FileInputStream(goalFilePath2));
    		
    		BufferedImage redImage1 = ImageIO.read(new FileInputStream(filePath + "myresult/1_red.bmp"));
    		BufferedImage redImage2 = ImageIO.read(new FileInputStream(filePath + "myresult/2_red.bmp"));

    		assertEquals(true, isEqual(redImage1Goal, redImage1));
    		assertEquals(true, isEqual(redImage2Goal, redImage2));
    		
		} catch (IOException e) {
			logger.log(Level.WARNING, "testRed");
		}
    }
    
    /**
	 * Test of Chanel Blue Image
	 */
    @Test
    public void testBlue() {
    	Logger logger = Logger.getLogger(logtext);
    	try {
    		String goalFilePath1 = filePath + "goal/1_blue_goal.bmp";
    		String goalFilePath2 = filePath + "goal/2_blue_goal.bmp";
    		
    		BufferedImage blueImage1Goal = ImageIO.read(new FileInputStream(goalFilePath1));
    		BufferedImage blueImage2Goal = ImageIO.read(new FileInputStream(goalFilePath2));
    		
    		BufferedImage blueImage1 = ImageIO.read(new FileInputStream(filePath + "myresult/1_blue.bmp"));
    		BufferedImage blueImage2 = ImageIO.read(new FileInputStream(filePath + "myresult/2_blue.bmp"));

    		assertEquals(true, isEqual(blueImage1Goal, blueImage1));

    		assertEquals(true, isEqual(blueImage2Goal, blueImage2));
    		
		} catch (IOException e) {
			logger.log(Level.WARNING, "testBlue");
		}
    }
    
    /**
	 * Test of Chanel Green Image
	 */
    @Test
    public void testGreen() {
    	Logger logger = Logger.getLogger(logtext);
    	try {
    		String goalFilePath1 = filePath + "goal/1_green_goal.bmp";
    		String goalFilePath2 = filePath + "goal/2_green_goal.bmp";
    		
    		BufferedImage greenImage1Goal = ImageIO.read(new FileInputStream(goalFilePath1));
    		BufferedImage greenImage2Goal = ImageIO.read(new FileInputStream(goalFilePath2));
    		
    		BufferedImage greenImage1 = ImageIO.read(new FileInputStream(filePath + "myresult/1_green.bmp"));
    		BufferedImage greenImage2 = ImageIO.read(new FileInputStream(filePath + "myresult/2_green.bmp"));

    		assertEquals(true, isEqual(greenImage1Goal, greenImage1));

    		assertEquals(true, isEqual(greenImage2Goal, greenImage2));
    		
		} catch (IOException e) {
			logger.log(Level.WARNING, "testGreen");
		}
    }
    
    /**
	 * Test of Gray Scale Image
	 */
    @Test
    public void testGray() {
    	Logger logger = Logger.getLogger(logtext);
    	try {
    		String goalFilePath1 = filePath + "goal/1_gray_goal.bmp";
    		String goalFilePath2 = filePath + "goal/2_gray_goal.bmp";
    		
    		BufferedImage grayImage1Goal = ImageIO.read(new FileInputStream(goalFilePath1));
    		BufferedImage grayImage2Goal = ImageIO.read(new FileInputStream(goalFilePath2));
    		
    		BufferedImage grayImage1 = ImageIO.read(new FileInputStream(filePath + "myresult/1_gray.bmp"));
    		BufferedImage grayImage2 = ImageIO.read(new FileInputStream(filePath + "myresult/2_gray.bmp"));

    		assertEquals(true, isEqual(grayImage1Goal, grayImage1));

    		assertEquals(true, isEqual(grayImage2Goal, grayImage2));
    		
		} catch (IOException e) {
			logger.log(Level.WARNING, "testGray");
		}
    }
    
}


