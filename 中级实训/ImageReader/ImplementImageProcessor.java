import java.awt.*;
import java.awt.Image;
import java.awt.image.*;
import java.util.logging.*;

import imagereader.*;

public class ImplementImageProcessor implements IImageProcessor {

	String logText = "log.text";
    /**
     * showChanelR
     * @param sourceImage
     * @return the red channel image of the source
     */
    public Image showChanelR(Image sourceImage) {
    	Logger logger = Logger.getLogger(logText);
        try {
            ImageProducer producer = 
                new FilteredImageSource(sourceImage.getSource(), new MyRGBFilter(MyRGBFilter.RED));
            return Toolkit.getDefaultToolkit().createImage(producer);
        } catch (Exception e) {
            logger.log(Level.WARNING, "showChanelR");
        }
        return null;
    }

    /**
     * showChanelG
     * @param sourceImage
     * @return the green channel image of the source
     */
    public Image showChanelG(Image sourceImage) {
    	Logger logger = Logger.getLogger(logText);
        try {
            ImageProducer producer = 
                new FilteredImageSource(sourceImage.getSource(), new MyRGBFilter(MyRGBFilter.GREEN));
            return Toolkit.getDefaultToolkit().createImage(producer);
        } catch (Exception e) {
            logger.log(Level.WARNING, "showChanelG");
        }
        return null;
    }

    /**
     * showChanelB
     * @param sourceImage
     * @return the blue channel image of the source
     */
    public Image showChanelB(Image sourceImage) {
    	Logger logger = Logger.getLogger(logText);
        try {
            ImageProducer producer = 
                new FilteredImageSource(sourceImage.getSource(), new MyRGBFilter(MyRGBFilter.BLUE));
            return Toolkit.getDefaultToolkit().createImage(producer);
        } catch (Exception e) {
            logger.log(Level.WARNING, "showChanelB");
        }
        return null;
    }

    /**
     * showGray
     * @param sourceImage
     * @return the grayscale image of the source
     */
    public Image showGray(Image sourceImage) {
    	Logger logger = Logger.getLogger(logText);
        try {
            ImageProducer producer = 
                new FilteredImageSource(sourceImage.getSource(), new MyGrayFilter());
            return Toolkit.getDefaultToolkit().createImage(producer);
        } catch (Exception e) {
            logger.log(Level.WARNING, "showGray");
        }
        return null;
    }
}

