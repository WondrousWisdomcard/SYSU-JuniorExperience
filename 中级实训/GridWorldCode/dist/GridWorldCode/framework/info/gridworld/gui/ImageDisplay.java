/* 
 * AP(r) Computer Science GridWorld Case Study:
 * Copyright(c) 2002-2006 College Entrance Examination Board 
 * (http://www.collegeboard.com).
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation.
 *
 * This code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * @author Julie Zelenski
 * @author Cay Horstmann
 */

package info.gridworld.gui;

import java.awt.Color;
import java.awt.Component;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Rectangle;
import java.awt.image.FilteredImageSource;
import java.awt.image.RGBImageFilter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import javax.imageio.ImageIO;

/**
 * An ImageDisplay displays an object as a tinted image from an image file whose
 * name matches the class name. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */

public class ImageDisplay extends AbstractDisplay
{
    private Class cl;
    private String imageFilename;
    private static final String imageExtension = ".gif";
    private Map<String, Image> tintedVersions = new HashMap<String, Image>();

    /**
     * Constructs an object that knows how to display an image. Looks for the
     * named file first in the jar file, then in the current directory.
     * @param imageFilename name of file containing image
     */
    public ImageDisplay(Class cl) throws IOException
    {
        this.cl = cl;
        imageFilename = cl.getName().replace('.', '/');
        URL url = cl.getClassLoader().getResource(
                imageFilename + imageExtension);

        if (url == null)
            throw new FileNotFoundException(imageFilename + imageExtension
                    + " not found.");
        tintedVersions.put("", ImageIO.read(url));
    }

    /**
     * Draws a unit-length object facing North. This implementation draws an
     * object by tinting, scaling, and rotating the image in the image file.
     * @param obj object we want to draw
     * @param comp the component we're drawing on
     * @param g2 drawing surface
     */
    public void draw(Object obj, Component comp, Graphics2D g2)
    {
        Color color;
        if (obj == null)
            color = null;
        else
            color = (Color) getProperty(obj, "color");
        String imageSuffix = (String) getProperty(obj, "imageSuffix");
        if (imageSuffix == null)
            imageSuffix = "";
        // Compose image with color using an image filter.
        Image tinted = tintedVersions.get(color + imageSuffix);
        if (tinted == null) // not cached, need new filter for color
        {
            Image untinted = tintedVersions.get(imageSuffix);
            if (untinted == null) // not cached, need to fetch
            {
                try
                {
                    URL url = cl.getClassLoader().getResource(
                            imageFilename + imageSuffix + imageExtension);
                    if (url == null)
                        throw new FileNotFoundException(imageFilename
                                + imageSuffix + imageExtension + " not found.");
                    untinted = ImageIO.read(url);
                    tintedVersions.put(imageSuffix, untinted);
                }
                catch (IOException ex)
                {
                    untinted = tintedVersions.get("");
                }
            }
            if (color == null)
                tinted = untinted;
            else
            {
                FilteredImageSource src = new FilteredImageSource(untinted
                    .getSource(), new TintFilter(color));
                tinted = comp.createImage(src);
                // Cache tinted image in map by color, we're likely to need it
                // again.
                tintedVersions.put(color + imageSuffix, tinted);
            }
        }
        int width = tinted.getWidth(null);
        int height = tinted.getHeight(null);
        int size = Math.max(width, height);
        
        // Scale to shrink or enlarge the image to fit the size 1x1 cell.
        g2.scale(1.0 / size, 1.0 / size);
        g2.clip(new Rectangle(-width / 2, -height / 2, width, height));
        g2.drawImage(tinted, -width / 2, -height / 2, null);
    }

    /**
     * An image filter class that tints colors based on the tint provided to the
     * constructor (the color of an object).
     */
    private static class TintFilter extends RGBImageFilter
    {
        private int tintR, tintG, tintB;

        /**
         * Constructs an image filter for tinting colors in an image.
         * @param color the tint color
         */
        public TintFilter(Color color)
        {
            canFilterIndexColorModel = true;
            int rgb = color.getRGB();
            tintR = (rgb >> 16) & 0xff;
            tintG = (rgb >> 8) & 0xff;
            tintB = rgb & 0xff;
        }

        public int filterRGB(int x, int y, int argb)
        {
            // Separate pixel into its RGB coomponents.
            int alpha = (argb >> 24) & 0xff;
            int red = (argb >> 16) & 0xff;
            int green = (argb >> 8) & 0xff;
            int blue = argb & 0xff;
            // Use NTSC/PAL algorithm to convert RGB to gray level
            double lum = (0.2989 * red + 0.5866 * green + 0.1144 * blue) / 255;

            // interpolate between tint and pixel color. Pixels with
            // gray level 0.5 are colored with the tint color,
            // white and black pixels stay unchanged.
            // We use a quadratic interpolation function
            // f(x) = 1 - 4 * (x - 0.5)^2 that has
            // the property f(0) = f(1) = 0, f(0.5) = 1
            
            // Note: Julie's algorithm used a linear interpolation
            // function f(x) = min(2 - 2 * x, 2 * x);
            // and it interpolated between tint and 
            // (lum < 0.5 ? black : white)

            double scale = 1 - (4 * ((lum - 0.5) * (lum - 0.5)));
            
            red = (int) (tintR * scale + red * (1 - scale));
            green = (int) (tintG * scale + green * (1 - scale));
            blue = (int) (tintB * scale + blue * (1 - scale));
            return (alpha << 24) | (red << 16) | (green << 8) | blue;
        }
    }
 }
