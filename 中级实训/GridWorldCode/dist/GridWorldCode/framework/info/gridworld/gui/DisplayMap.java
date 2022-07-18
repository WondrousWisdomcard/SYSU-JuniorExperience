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

import java.awt.Component;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.geom.AffineTransform;
import java.util.HashMap;

import javax.swing.Icon;

/**
 * <code>DisplayMap</code> is a collection that maps grid occupant
 * classes to objects that know how to display them. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */
public class DisplayMap
{
    private HashMap<Class, Display> map = new HashMap<Class, Display>();
    private Display defaultDisplay = new DefaultDisplay();

    /**
     * Associates a display object with a grid occupant class. 
     * @param the occupant class
     * @return the ImageDisplay or (classname)Display object to display it, 
     * or null if none was found
     */

    private Display createDisplay(Class cl)
    {
        try
        {
            String className = cl.getName();
            Class dcl = Class.forName(className + "Display");
            if (Display.class.isAssignableFrom(dcl))
            {
                Display display = (Display) dcl.newInstance();
                map.put(cl, display);
                return display;
            }
        }
        catch (Exception e)
        {
            // oh well...
        }

        try
        {
            ImageDisplay display = new ImageDisplay(cl);
            map.put(cl, display);
            return display;
        }
        catch (Exception e)
        {
            // oh well...
        }

        return null;
    }

    /**
     * Finds a display class that knows how to display the given object.
     * @param obj the object to display
     */
    public Display findDisplayFor(Class cl)
    {
        // Go up through the class hierarchy for obj and see
        // if there is a display for its class or superclasses.

        if (cl == Object.class)
            return defaultDisplay;
        Display display = map.get(cl);
        if (display != null)
            return display;
        display = createDisplay(cl);
        if (display != null)
        {
            map.put(cl, display);
            return display;
        }
        display = findDisplayFor(cl.getSuperclass());
        map.put(cl, display);
        return display;
    }

    /**
     * Gets an icon to display a class in a menu
     * @param cl the class
     * @param w the icon width
     * @param h the icon height
     * @return the icon
     */
    public Icon getIcon(Class cl, int w, int h)
    {
        return new DisplayIcon(cl, w, h);
    }

    private class DisplayIcon implements Icon
    {
        private Display displayObj;
        private int width, height;

        public DisplayIcon(Class cl, int w, int h)
        {
            displayObj = findDisplayFor(cl);
            width = w;
            height = h;
        }

        public int getIconWidth()
        {
            return width;
        }

        public int getIconHeight()
        {
            return height;
        }

        public void paintIcon(Component comp, Graphics g, int x, int y)
        {
            Graphics2D g2 = (Graphics2D) g;
            AffineTransform savedTransform = g2.getTransform(); // save current
            displayObj.draw(null, comp, g2, new Rectangle(x, y, getIconWidth(),
                    getIconHeight()));
            g2.setTransform(savedTransform); // restore coordinate system
        }
    }
}
