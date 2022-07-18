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
 * @author Alyce Brady
 * @author Jeff Raab, Northeastern University
 * @author Cay Horstmann
 */

package info.gridworld.gui;

import java.awt.Color;
import java.awt.Font;
import java.awt.Component;
import java.awt.font.FontRenderContext;
import java.awt.font.LineMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.Rectangle2D;
import java.awt.Rectangle;

/**
 * The DefaultDisplay draws the object's text property with a background color
 * given by the object's color property. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */
public class DefaultDisplay implements Display
{
    private static final int MAX_TEXT_LENGTH = 8;

    /**
     * Draw the given object. This implementation draws a string with
     * a background color. The background color is the value
     * of the color property, or, if there is no such property
     * and the object is an instance of Color, the object itself.
     * The string is the text property, or if there is no such
     * property, the result of calling toString. The string
     * is clipped to 8 characters.
     * @param obj object we want to draw
     * @param comp component on which to draw
     * @param g2 drawing surface
     * @param rect rectangle in which to draw
     */
    public void draw(Object obj, Component comp, Graphics2D g2, Rectangle rect)
    {
        Color color = (Color) AbstractDisplay.getProperty(obj, "color");
        if (color == null && obj instanceof Color)
            color = (Color) obj;
        Color textColor = (Color) AbstractDisplay.getProperty(obj, "textColor");
        if (textColor == null) textColor = Color.BLACK;
        if (color != null)
        {
            g2.setPaint(color);
            g2.fill(rect);

            if (color.equals(textColor))
            {
                textColor = new Color(
                        255 - textColor.getRed(),
                        255 - textColor.getGreen(), 
                        255 - textColor.getBlue()); 
            }
        }
        String text = (String) AbstractDisplay.getProperty(obj, "text");
        if (text == null && !(obj instanceof Color))
        {
            text = "" + obj;
        }
        if (text == null) return;
        if (text.length() > MAX_TEXT_LENGTH)
            text = text.substring(0, MAX_TEXT_LENGTH) + "...";
        paintCenteredText(g2, text, rect, 0.8, textColor);
    }

    /**
     * Paint a horizontally and vertically-centered text string.
     * @param g2 drawing surface
     * @param s string to draw (centered)
     * @param rect the bounding rectangle
     * @param fontHeight the desired height of the font. (The font will be
     * shrunk in increments of sqrt(2)/2 if the text is too large.)
     * @param color the color in which to draw the text
     */
    protected void paintCenteredText(Graphics2D g2, String s, Rectangle rect,
            double fontHeight, Color color)
    {
        g2 = (Graphics2D) g2.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setPaint(color);
        Rectangle2D bounds = null;
        LineMetrics lm = null;
        boolean done = false;
        // shrink font in increments of sqrt(2)/2 until string fits
        while (!done)
        {
            g2.setFont(new Font("SansSerif", Font.BOLD,
                    (int) (fontHeight * rect.height)));
            FontRenderContext frc = g2.getFontRenderContext();
            bounds = g2.getFont().getStringBounds(s, frc);
            if (bounds.getWidth() > rect.getWidth())
                fontHeight = fontHeight * Math.sqrt(2) / 2;
            else
            {
                done = true;
                lm = g2.getFont().getLineMetrics(s, frc);
            }
        }
        float centerX = rect.x + rect.width / 2;
        float centerY = rect.y + rect.height / 2;
        float leftX = centerX - (float) bounds.getWidth() / 2;
        float baselineY = centerY - lm.getHeight() / 2 + lm.getAscent();
        g2.drawString(s, leftX, baselineY);
        g2.dispose();
    }
}
