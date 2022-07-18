import java.awt.image.*;

// 过滤器 API
// https://www.apiref.com/java11-zh/java.desktop/java/awt/image/RGBImageFilter.html
// https://www.apiref.com/java11-zh/java.desktop/java/awt/image/RGBImageFilter.html#filterRGB(int,int,int)

/**
 * Gray Filter 灰度像素过滤器
 */
public class MyGrayFilter extends RGBImageFilter {

    public MyGrayFilter(){
        canFilterIndexColorModel = true;
    }

    /**
     * filterRGB: implement abstract method from RGBImageFilter
     * 将彩色图转换成灰度图，建议采用NTSC推荐的彩色图到灰度图的转换公式：
     * I = 0.299 * R + 0.587 * G + 0.114 *B
     * 其中R,G,B分别为红、绿、蓝通道的颜色值，
     * 将三个色彩通道的颜色值改为这个值即可。
     * @param x
     * @param y
     * @param rgb origin color
     * @return the color of pixel after *NTSC* gray filtering
     */
    public int filterRGB(int x, int y, int rgb){
        int r = (rgb & 0x00ff0000) >> 16;
        int g = (rgb & 0x0000ff00) >> 8;
        int b = (rgb & 0x000000ff);
        int c = (int)(0.299 * r + 0.587 * g + 0.114 * b);
        return (c << 16 | c << 8 | c | 0xff000000);
    }
}
