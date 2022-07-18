import java.awt.image.*;

// 过滤器 API
// https://www.apiref.com/java11-zh/java.desktop/java/awt/image/RGBImageFilter.html
// https://www.apiref.com/java11-zh/java.desktop/java/awt/image/RGBImageFilter.html#filterRGB(int,int,int)

/**
 * RGB Filter 红/绿/蓝像素过滤器
 */
public class MyRGBFilter extends RGBImageFilter {

    public static final int RED = 0; 
    public static final int GREEN = 1; 
    public static final int BLUE = 2; 

    private int color;
    /**
     * Constructor
     * @param color RED or GREEN or BLUE
     */
    public MyRGBFilter(int color){
        this.color = color;
        canFilterIndexColorModel = true;
    }

    /**
     * filterRGB: implement abstract method from RGBImageFilter
     * @param x
     * @param y
     * @param rgb origin color
     * @return the color of pixel after red/green/blue filtering
     */
	@Override
	public int filterRGB(int x, int y, int rgb) {
		if(color == RED){
            return (rgb & 0xffff0000);
        }
        else if(color == GREEN){
            return (rgb & 0xff00ff00);
        }
        else if(color == BLUE){
            return (rgb & 0xff0000ff);
        }
        else{
            return rgb;
        }
	}
}
