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

import info.gridworld.grid.*;
import info.gridworld.world.World;

import java.awt.Dimension;
import java.awt.Point;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.lang.reflect.Modifier;
import java.util.Comparator;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.TreeSet;

import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.*;

/**
 * The GUIController controls the behavior in a WorldFrame. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */

public class GUIController<T>
{
    public static final int INDEFINITE = 0, FIXED_STEPS = 1, PROMPT_STEPS = 2;

    private static final int MIN_DELAY_MSECS = 10, MAX_DELAY_MSECS = 1000;
    private static final int INITIAL_DELAY = MIN_DELAY_MSECS
            + (MAX_DELAY_MSECS - MIN_DELAY_MSECS) / 2;

    private Timer timer;
    private JButton stepButton, runButton, stopButton;
    private JComponent controlPanel;
    private GridPanel display;
    private WorldFrame<T> parentFrame;
    private int numStepsToRun, numStepsSoFar;
    private ResourceBundle resources;
    private DisplayMap displayMap;
    private boolean running;
    private Set<Class> occupantClasses;

    /**
     * Creates a new controller tied to the specified display and gui
     * frame.
     * @param parent the frame for the world window
     * @param disp the panel that displays the grid
     * @param displayMap the map for occupant displays
     * @param res the resource bundle for message display
     */
    public GUIController(WorldFrame<T> parent, GridPanel disp,
            DisplayMap displayMap, ResourceBundle res)
    {
        resources = res;
        display = disp;
        parentFrame = parent;
        this.displayMap = displayMap;
        makeControls();

        occupantClasses = new TreeSet<Class>(new Comparator<Class>()
        {
            public int compare(Class a, Class b)
            {
                return a.getName().compareTo(b.getName());
            }
        });

        World<T> world = parentFrame.getWorld();
        Grid<T> gr = world.getGrid();
        for (Location loc : gr.getOccupiedLocations())
            addOccupant(gr.get(loc));
        for (String name : world.getOccupantClasses())
            try
            {
                occupantClasses.add(Class.forName(name));
            }
            catch (Exception ex)
            {
                ex.printStackTrace();
            }

        timer = new Timer(INITIAL_DELAY, new ActionListener()
        {
            public void actionPerformed(ActionEvent evt)
            {
                step();
            }
        });

        display.addMouseListener(new MouseAdapter()
        {
            public void mousePressed(MouseEvent evt)
            {
                Grid<T> gr = parentFrame.getWorld().getGrid();
                Location loc = display.locationForPoint(evt.getPoint());
                if (loc != null && gr.isValid(loc) && !isRunning())
                {
                    display.setCurrentLocation(loc);
                    locationClicked();
                }
            }
        });
        stop();
    }

    /**
     * Advances the world one step.
     */
    public void step()
    {
        parentFrame.getWorld().step();
        parentFrame.repaint();
        if (++numStepsSoFar == numStepsToRun)
            stop();
        Grid<T> gr = parentFrame.getWorld().getGrid();

        for (Location loc : gr.getOccupiedLocations())
            addOccupant(gr.get(loc));
    }

    private void addOccupant(T occupant)
    {
        Class cl = occupant.getClass();
        do
        {
            if ((cl.getModifiers() & Modifier.ABSTRACT) == 0)
                occupantClasses.add(cl);
            cl = cl.getSuperclass();
        }
        while (cl != Object.class);
    }

    /**
     * Starts a timer to repeatedly carry out steps at the speed currently
     * indicated by the speed slider up Depending on the run option, it will
     * either carry out steps for some fixed number or indefinitely
     * until stopped.
     */
    public void run()
    {
        display.setToolTipsEnabled(false); // hide tool tips while running
        parentFrame.setRunMenuItemsEnabled(false);
        stopButton.setEnabled(true);
        stepButton.setEnabled(false);
        runButton.setEnabled(false);
        numStepsSoFar = 0;
        timer.start();
        running = true;
    }

    /**
     * Stops any existing timer currently carrying out steps.
     */
    public void stop()
    {
        display.setToolTipsEnabled(true);
        parentFrame.setRunMenuItemsEnabled(true);
        timer.stop();
        stopButton.setEnabled(false);
        runButton.setEnabled(true);
        stepButton.setEnabled(true);
        running = false;
    }

    public boolean isRunning()
    {
        return running;
    }

    /**
     * Builds the panel with the various controls (buttons and
     * slider).
     */
    private void makeControls()
    {
        controlPanel = new JPanel();
        stepButton = new JButton(resources.getString("button.gui.step"));
        runButton = new JButton(resources.getString("button.gui.run"));
        stopButton = new JButton(resources.getString("button.gui.stop"));
        
        controlPanel.setLayout(new BoxLayout(controlPanel, BoxLayout.X_AXIS));
        controlPanel.setBorder(BorderFactory.createEtchedBorder());
        
        Dimension spacer = new Dimension(5, stepButton.getPreferredSize().height + 10);
        
        controlPanel.add(Box.createRigidArea(spacer));

        controlPanel.add(stepButton);
        controlPanel.add(Box.createRigidArea(spacer));
        controlPanel.add(runButton);
        controlPanel.add(Box.createRigidArea(spacer));
        controlPanel.add(stopButton);
        runButton.setEnabled(false);
        stepButton.setEnabled(false);
        stopButton.setEnabled(false);

        controlPanel.add(Box.createRigidArea(spacer));
        controlPanel.add(new JLabel(resources.getString("slider.gui.slow")));
        JSlider speedSlider = new JSlider(MIN_DELAY_MSECS, MAX_DELAY_MSECS,
                INITIAL_DELAY);
        speedSlider.setInverted(true);
        speedSlider.setPreferredSize(new Dimension(100, speedSlider
                .getPreferredSize().height));
        speedSlider.setMaximumSize(speedSlider.getPreferredSize());

        // remove control PAGE_UP, PAGE_DOWN from slider--they should be used
        // for zoom
        InputMap map = speedSlider.getInputMap();
        while (map != null)
        {
            map.remove(KeyStroke.getKeyStroke("control PAGE_UP"));
            map.remove(KeyStroke.getKeyStroke("control PAGE_DOWN"));
            map = map.getParent();
        }

        controlPanel.add(speedSlider);
        controlPanel.add(new JLabel(resources.getString("slider.gui.fast")));
        controlPanel.add(Box.createRigidArea(new Dimension(5, 0)));

        stepButton.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                step();
            }
        });
        runButton.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                run();
            }
        });
        stopButton.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                stop();
            }
        });
        speedSlider.addChangeListener(new ChangeListener()
        {
            public void stateChanged(ChangeEvent evt)
            {
                timer.setDelay(((JSlider) evt.getSource()).getValue());
            }
        });
    }

    /**
     * Returns the panel containing the controls.
     * @return the control panel
     */
    public JComponent controlPanel()
    {
        return controlPanel;
    }

    /**
     * Callback on mousePressed when editing a grid.
     */
    private void locationClicked()
    {
        World<T> world = parentFrame.getWorld();
        Location loc = display.getCurrentLocation();
        if (loc != null && !world.locationClicked(loc))
            editLocation();
        parentFrame.repaint();
    }

    /**
     * Edits the contents of the current location, by displaying the constructor
     * or method menu.
     */
    public void editLocation()
    {
        World<T> world = parentFrame.getWorld();

        Location loc = display.getCurrentLocation();
        if (loc != null)
        {
            T occupant = world.getGrid().get(loc);
            if (occupant == null)
            {
                MenuMaker<T> maker = new MenuMaker<T>(parentFrame, resources,
                        displayMap);
                JPopupMenu popup = maker.makeConstructorMenu(occupantClasses,
                        loc);
                Point p = display.pointForLocation(loc);
                popup.show(display, p.x, p.y);
            }
            else
            {
                MenuMaker<T> maker = new MenuMaker<T>(parentFrame, resources,
                        displayMap);
                JPopupMenu popup = maker.makeMethodMenu(occupant, loc);
                Point p = display.pointForLocation(loc);
                popup.show(display, p.x, p.y);
            }
        }
        parentFrame.repaint();
    }

    /**
     * Edits the contents of the current location, by displaying the constructor
     * or method menu.
     */
    public void deleteLocation()
    {
        World<T> world = parentFrame.getWorld();
        Location loc = display.getCurrentLocation();
        if (loc != null)
        {
            world.remove(loc);
            parentFrame.repaint();
        }
    }
}
