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
 * @author Cay Horstmann
 */

package info.gridworld.gui;

import java.awt.Graphics2D;
import java.awt.Component;
import java.awt.Rectangle;

/**
 * The <code>Display</code> interface contains the method needed to display a
 * grid object. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */
public interface Display
{
    /**
     * Method invoked to draw an object.
     * @param obj object we want to draw
     * @param comp component on which to draw
     * @param g2 drawing surface
     * @param rect rectangle in which to draw
     */
    void draw(Object obj, Component c, Graphics2D g2, Rectangle rect);
}
