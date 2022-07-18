/* 
 * AP(r) Computer Science GridWorld Case Study:
 * Copyright(c) 2005-2006 Cay S. Horstmann (http://horstmann.com)
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
 * @author Cay Horstmann
 */

package info.gridworld.gui;

import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;

import java.awt.Color;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.beans.PropertyEditor;
import java.beans.PropertyEditorManager;
import java.beans.PropertyEditorSupport;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.ResourceBundle;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

/**
 * Makes the menus for constructing new occupants and grids, and for invoking
 * methods on existing occupants. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */
public class MenuMaker<T>
{
    /**
     * Constructs a menu maker for a given world.
     * @param parent the frame in which the world is displayed
     * @param resources the resource bundle
     * @param displayMap the display map
     */
    public MenuMaker(WorldFrame<T> parent, ResourceBundle resources,
            DisplayMap displayMap)
    {
        this.parent = parent;
        this.resources = resources;
        this.displayMap = displayMap;
    }

    /**
     * Makes a menu that displays all public methods of an object
     * @param occupant the object whose methods should be displayed
     * @param loc the location of the occupant
     * @return the menu to pop up
     */
    public JPopupMenu makeMethodMenu(T occupant, Location loc)
    {
        this.occupant = occupant;
        this.currentLocation = loc;
        JPopupMenu menu = new JPopupMenu();
        Method[] methods = getMethods();
        Class oldDcl = null;
        for (int i = 0; i < methods.length; i++)
        {
            Class dcl = methods[i].getDeclaringClass();
            if (dcl != Object.class)
            {
                if (i > 0 && dcl != oldDcl)
                    menu.addSeparator();
                menu.add(new MethodItem(methods[i]));
            }
            oldDcl = dcl;
        }
        return menu;
    }

    /**
     * Makes a menu that displays all public constructors of a collection of
     * classes.
     * @param classes the classes whose constructors should be displayed
     * @param loc the location of the occupant to be constructed
     * @return the menu to pop up
     */
    public JPopupMenu makeConstructorMenu(Collection<Class> classes,
            Location loc)
    {
        this.currentLocation = loc;
        JPopupMenu menu = new JPopupMenu();
        boolean first = true;
        Iterator<Class> iter = classes.iterator();
        while (iter.hasNext())
        {
            if (first)
                first = false;
            else
                menu.addSeparator();
            Class cl = iter.next();
            Constructor[] cons = (Constructor[]) cl.getConstructors();
            for (int i = 0; i < cons.length; i++)
            {
                menu.add(new OccupantConstructorItem(cons[i]));
            }
        }
        return menu;
    }

    /**
     * Adds menu items that call all public constructors of a collection of
     * classes to a menu
     * @param menu the menu to which the items should be added
     * @param classes the collection of classes
     */
    public void addConstructors(JMenu menu, Collection<Class> classes)
    {
        boolean first = true;
        Iterator<Class> iter = classes.iterator();
        while (iter.hasNext())
        {
            if (first)
                first = false;
            else
                menu.addSeparator();
            Class cl = iter.next();
            Constructor[] cons = cl.getConstructors();
            for (int i = 0; i < cons.length; i++)
            {
                menu.add(new GridConstructorItem(cons[i]));
            }
        }
    }

    private Method[] getMethods()
    {
        Class cl = occupant.getClass();
        Method[] methods = cl.getMethods();

        Arrays.sort(methods, new Comparator<Method>()
        {
            public int compare(Method m1, Method m2)
            {
                int d1 = depth(m1.getDeclaringClass());
                int d2 = depth(m2.getDeclaringClass());
                if (d1 != d2)
                    return d2 - d1;
                int d = m1.getName().compareTo(m2.getName());
                if (d != 0)
                    return d;
                d1 = m1.getParameterTypes().length;
                d2 = m2.getParameterTypes().length;
                return d1 - d2;
            }

            private int depth(Class cl)
            {
                if (cl == null)
                    return 0;
                else
                    return 1 + depth(cl.getSuperclass());
            }
        });
        return methods;
    }

    /**
     * A menu item that shows a method or constructor.
     */
    private class MCItem extends JMenuItem
    {
        public String getDisplayString(Class retType, String name,
                Class[] paramTypes)
        {
            StringBuffer b = new StringBuffer();
            b.append("<html>");
            if (retType != null)
                appendTypeName(b, retType.getName());
            b.append(" <font color='blue'>");
            appendTypeName(b, name);
            b.append("</font>( ");
            for (int i = 0; i < paramTypes.length; i++)
            {
                if (i > 0)
                    b.append(", ");
                appendTypeName(b, paramTypes[i].getName());
            }
            b.append(" )</html>");
            return b.toString();
        }

        public void appendTypeName(StringBuffer b, String name)
        {
            int i = name.lastIndexOf('.');
            if (i >= 0)
            {
                String prefix = name.substring(0, i + 1);
                if (!prefix.equals("java.lang"))
                {
                    b.append("<font color='gray'>");
                    b.append(prefix);
                    b.append("</font>");
                }
                b.append(name.substring(i + 1));
            }
            else
                b.append(name);
        }

        public Object makeDefaultValue(Class type)
        {
            if (type == int.class)
                return new Integer(0);
            else if (type == boolean.class)
                return Boolean.FALSE;
            else if (type == double.class)
                return new Double(0);
            else if (type == String.class)
                return "";
            else if (type == Color.class)
                return Color.BLACK;
            else if (type == Location.class)
                return currentLocation;
            else if (Grid.class.isAssignableFrom(type))
                return currentGrid;
            else
            {
                try
                {
                    return type.newInstance();
                }
                catch (Exception ex)
                {
                    return null;
                }
            }
        }
    }

    private abstract class ConstructorItem extends MCItem
    {
        public ConstructorItem(Constructor c)
        {
            setText(getDisplayString(null, c.getDeclaringClass().getName(), c
                    .getParameterTypes()));
            this.c = c;
        }

        public Object invokeConstructor()
        {
            Class[] types = c.getParameterTypes();
            Object[] values = new Object[types.length];

            for (int i = 0; i < types.length; i++)
            {
                values[i] = makeDefaultValue(types[i]);
            }

            if (types.length > 0)
            {
                PropertySheet sheet = new PropertySheet(types, values);
                JOptionPane.showMessageDialog(this, sheet, resources
                        .getString("dialog.method.params"),
                        JOptionPane.QUESTION_MESSAGE);
                values = sheet.getValues();
            }

            try
            {
                return c.newInstance(values);
            }
            catch (InvocationTargetException ex)
            {
                parent.new GUIExceptionHandler().handle(ex.getCause());
                return null;
            }
            catch (Exception ex)
            {
                parent.new GUIExceptionHandler().handle(ex);
                return null;
            }
        }

        private Constructor c;
    }

    private class OccupantConstructorItem extends ConstructorItem implements
            ActionListener
    {
        public OccupantConstructorItem(Constructor c)
        {
            super(c);
            addActionListener(this);
            setIcon(displayMap.getIcon(c.getDeclaringClass(), 16, 16));
        }

        @SuppressWarnings("unchecked")
        public void actionPerformed(ActionEvent event)
        {
            T result = (T) invokeConstructor();
            parent.getWorld().add(currentLocation, result);
            parent.repaint();
        }
    }

    private class GridConstructorItem extends ConstructorItem implements
            ActionListener
    {
        public GridConstructorItem(Constructor c)
        {
            super(c);
            addActionListener(this);
            setIcon(displayMap.getIcon(c.getDeclaringClass(), 16, 16));
        }

        @SuppressWarnings("unchecked")
        public void actionPerformed(ActionEvent event)
        {
            Grid<T> newGrid = (Grid<T>) invokeConstructor(); 
            parent.setGrid(newGrid);
        }
    }

    private class MethodItem extends MCItem implements ActionListener
    {
        public MethodItem(Method m)
        {
            setText(getDisplayString(m.getReturnType(), m.getName(), m
                    .getParameterTypes()));
            this.m = m;
            addActionListener(this);
            setIcon(displayMap.getIcon(m.getDeclaringClass(), 16, 16));
        }

        public void actionPerformed(ActionEvent event)
        {
            Class[] types = m.getParameterTypes();
            Object[] values = new Object[types.length];

            for (int i = 0; i < types.length; i++)
            {
                values[i] = makeDefaultValue(types[i]);
            }

            if (types.length > 0)
            {
                PropertySheet sheet = new PropertySheet(types, values);
                JOptionPane.showMessageDialog(this, sheet, resources
                        .getString("dialog.method.params"),
                        JOptionPane.QUESTION_MESSAGE);
                values = sheet.getValues();
            }

            try
            {
                Object result = m.invoke(occupant, values);
                parent.repaint();
                if (m.getReturnType() != void.class)
                {
                    String resultString = result.toString();
                    Object resultObject;
                    final int MAX_LENGTH = 50;
                    final int MAX_HEIGHT = 10;
                    if (resultString.length() < MAX_LENGTH)
                        resultObject = resultString;
                    else
                    {
                        int rows = Math.min(MAX_HEIGHT, 1
                                + resultString.length() / MAX_LENGTH);
                        JTextArea pane = new JTextArea(rows, MAX_LENGTH);
                        pane.setText(resultString);
                        pane.setLineWrap(true);
                        resultObject = new JScrollPane(pane);
                    }
                    JOptionPane.showMessageDialog(parent, resultObject,
                            resources.getString("dialog.method.return"),
                            JOptionPane.INFORMATION_MESSAGE);
                }
            }
            catch (InvocationTargetException ex)
            {
                parent.new GUIExceptionHandler().handle(ex.getCause());
            }
            catch (Exception ex)
            {
                parent.new GUIExceptionHandler().handle(ex);
            }
        }

        private Method m;
    }

    private T occupant;
    private Grid currentGrid;
    private Location currentLocation;
    private WorldFrame<T> parent;
    private DisplayMap displayMap;
    private ResourceBundle resources;
}

class PropertySheet extends JPanel
{
    /**
     * Constructs a property sheet that shows the editable properties of a given
     * object.
     * @param object the object whose properties are being edited
     */
    public PropertySheet(Class[] types, Object[] values)
    {
        this.values = values;
        editors = new PropertyEditor[types.length];
        setLayout(new FormLayout());
        for (int i = 0; i < values.length; i++)
        {
            JLabel label = new JLabel(types[i].getName());
            add(label);
            if (Grid.class.isAssignableFrom(types[i]))
            {
                label.setEnabled(false);
                add(new JPanel());
            }
            else
            {
                editors[i] = getEditor(types[i]);
                if (editors[i] != null)
                {
                    editors[i].setValue(values[i]);
                    add(getEditorComponent(editors[i]));
                }
                else
                    add(new JLabel("?"));
            }
        }
    }

    /**
     * Gets the property editor for a given property, and wires it so that it
     * updates the given object.
     * @param bean the object whose properties are being edited
     * @param descriptor the descriptor of the property to be edited
     * @return a property editor that edits the property with the given
     * descriptor and updates the given object
     */
    public PropertyEditor getEditor(Class type)
    {
        PropertyEditor editor;
        editor = defaultEditors.get(type);
        if (editor != null)
            return editor;
        editor = PropertyEditorManager.findEditor(type);
        return editor;
    }

    /**
     * Wraps a property editor into a component.
     * @param editor the editor to wrap
     * @return a button (if there is a custom editor), combo box (if the editor
     * has tags), or text field (otherwise)
     */
    public Component getEditorComponent(final PropertyEditor editor)
    {
        String[] tags = editor.getTags();
        String text = editor.getAsText();
        if (editor.supportsCustomEditor())
        {
            return editor.getCustomEditor();
        }
        else if (tags != null)
        {
            // make a combo box that shows all tags
            final JComboBox comboBox = new JComboBox(tags);
            comboBox.setSelectedItem(text);
            comboBox.addItemListener(new ItemListener()
            {
                public void itemStateChanged(ItemEvent event)
                {
                    if (event.getStateChange() == ItemEvent.SELECTED)
                        editor.setAsText((String) comboBox.getSelectedItem());
                }
            });
            return comboBox;
        }
        else
        {
            final JTextField textField = new JTextField(text, 10);
            textField.getDocument().addDocumentListener(new DocumentListener()
            {
                public void insertUpdate(DocumentEvent e)
                {
                    try
                    {
                        editor.setAsText(textField.getText());
                    }
                    catch (IllegalArgumentException exception)
                    {
                    }
                }

                public void removeUpdate(DocumentEvent e)
                {
                    try
                    {
                        editor.setAsText(textField.getText());
                    }
                    catch (IllegalArgumentException exception)
                    {
                    }
                }

                public void changedUpdate(DocumentEvent e)
                {
                }
            });
            return textField;
        }
    }

    public Object[] getValues()
    {
        for (int i = 0; i < editors.length; i++)
            if (editors[i] != null)
                values[i] = editors[i].getValue();
        return values;
    }

    private PropertyEditor[] editors;
    private Object[] values;

    private static Map<Class, PropertyEditor> defaultEditors;

    // workaround for Web Start bug
    public static class StringEditor extends PropertyEditorSupport
    {
        public String getAsText()
        {
            return (String) getValue();
        }

        public void setAsText(String s)
        {
            setValue(s);
        }
    }

    static
    {
        defaultEditors = new HashMap<Class, PropertyEditor>();
        defaultEditors.put(String.class, new StringEditor());
        defaultEditors.put(Location.class, new LocationEditor());
        defaultEditors.put(Color.class, new ColorEditor());
    }
}
