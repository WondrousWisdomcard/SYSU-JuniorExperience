import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.awt.*;
import java.io.*;
import java.awt.image.*;
import javax.imageio.*;
import java.util.logging.*;

import imagereader.*;

public class ImplementImageIO implements IImageIO {

    FileInputStream in;

    /**
     * .bmp 文件头（分别为14字节和40字节）
     * 参考：https://www.cnblogs.com/CZM-/p/5388553.html 
     * */
    byte[] bitmapFileHeader = new byte[14];
    byte[] bitmapInfoHeader = new byte[40];

    int width = 0;      // 图片宽度（像素为单位）
    int height = 0;     // 图片高度（像素为单位）
    int pixelNum = 0;   // 像素颜色模式：RGB / 灰度图
    int alignNum = 0;   // 每一行的空字节补齐位数

    int[] imageArray;
    Image image;

    /**
     * myRead implements from IImageIO
     * @param filePath
     * @return the image data read from a .bmp file
     */
    public Image myRead(String filePath) {

		Logger logger = Logger.getLogger("log.text");
        try {
            in = new FileInputStream(filePath);

			int t = 0;
			
            t = in.read(bitmapFileHeader);
            if(t != 14){
            	System.err.println("Bitmap file header read error");
            }
            
            t = in.read(bitmapInfoHeader);
            if(t != 40){
            	System.err.println("Bitmap info header read error");
            }
            
            width = getBiWidth();
            height = getBiHeight();
            pixelNum = getPixelNum();

            // 计算补齐位数
            if ((width * (pixelNum / 8)) % 4 != 0) {
                alignNum = 4 - (width * (pixelNum / 8)) % 4;
            }
            else {
            	alignNum = 0;
            }
            
            imageArray = new int[height * width];

            for (int i = height - 1; i >= 0; i--) {
                for (int j = 0; j < width; j++) {
                    int b = 0;                    
                    int g = 0;
                    int r = 0;

                    if (pixelNum == 24) {
                        b = in.read();
                        g = in.read();
                        r = in.read();                       
                    } else if (pixelNum == 8) {
                        b = in.read();
                        g = b;
                        r = b;                       
                    }

                    Color color = new Color(r, g, b);
                    imageArray[i * width + j] = color.getRGB();
                }
                long s = in.skip(alignNum);
                if(s != alignNum){
                	System.err.println("AlignNum skip error");
                }
            }
            ImageProducer producer = new MemoryImageSource(width, height, imageArray, 0, width);
            image = Toolkit.getDefaultToolkit().createImage(producer);
            in.close();
            return image;

        } catch (Exception e) {
            logger.log(Level.WARNING, "myRead");
        }
        return null;
    }

    /**
     * myWrite implements from IImageIO
     * @param image
     * @param filePath
     * @return store image data to filePath
     */
    public Image myWrite(Image image, String filePath) {
    	Logger logger = Logger.getLogger("log.text");
        try {
            BufferedImage buffer;

            int w = image.getWidth(null);
            int h = image.getHeight(null);

            if(pixelNum == 24){
                buffer = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);
            }
            else {
                buffer = new BufferedImage(w, h, BufferedImage.TYPE_BYTE_GRAY);
            }
        
            Graphics2D graphics = buffer.createGraphics();
            graphics.drawImage(image, 0, 0, null);

            File file = new File(filePath);
            ImageIO.write(buffer, "bmp", file);

        } catch (Exception e) {
            logger.log(Level.WARNING, "myWrite");
        }
        return null;
    }

    /**
     * getBiWidth
     * @return the width of the image
     */
    private int getBiWidth() {
        int w = 0;
        byte[] biWidth = new byte[4];
        for (int i = 0; i < 4; i++) {
            biWidth[3 - i] = bitmapInfoHeader[i + 4];
        }
        w = ByteBuffer.wrap(biWidth).getInt();
        return w;
    }

    /**
     * getBiHeight
     * @return the height of the image
     */
    private int getBiHeight() {
        int h = 0;
        byte[] biHeight = new byte[4];
        for (int i = 0; i < 4; i++) {
            biHeight[3 - i] = bitmapInfoHeader[i + 8];
        }
        h = ByteBuffer.wrap(biHeight).getInt();
        return h;
    }

    /**
     * getPixelNum
     * @return the color form of the image 24(rgb color) or 8(grayscale)
     */
    private int getPixelNum() {
        int pn = 0;
        byte[] biPixelNum = new byte[4];
        for (int i = 0; i < 2; i++) {
            biPixelNum[i] = 0;
        }
        for (int i = 0; i < 2; i++) {
            biPixelNum[3 - i] = bitmapInfoHeader[i + 14];
        }
       pn = ByteBuffer.wrap(biPixelNum).getInt();
        return pn;
    }

}
