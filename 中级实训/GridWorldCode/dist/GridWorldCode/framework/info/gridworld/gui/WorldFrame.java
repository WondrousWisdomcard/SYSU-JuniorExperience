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
 * @author Chris Nevison
 * @author Cay Horstmann
 */

package info.gridworld.gui;

import info.gridworld.actor.Actor;
import info.gridworld.actor.Bug;
import info.gridworld.actor.Flower;
import info.gridworld.actor.Rock;
import info.gridworld.grid.BoundedGrid;
import info.gridworld.grid.Grid;
import info.gridworld.grid.Location;
import info.gridworld.grid.UnboundedGrid;
import info.gridworld.world.World;
import info.gridworld.maze.*;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Frame;
import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.FileDialog;
import java.net.URL;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.MissingResourceException;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.TreeSet;

import javax.swing.AbstractButton;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JDialog;
import javax.swing.JEditorPane;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.KeyStroke;
import javax.swing.event.HyperlinkEvent;
import javax.swing.event.HyperlinkListener;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;

/**
 * The WorldFrame displays a World and allows manipulation of its occupants. <br />
 * This code is not tested on the AP CS A and AB exams. It contains GUI
 * implementation details that are not intended to be understood by AP CS
 * students.
 */
public class WorldFrame<T> extends JFrame {
	private GUIController<T> control;
	private GridPanel display;
	private JTextArea messageArea;
	private ArrayList<JMenuItem> menuItemsDisabledDuringRun;
	private World<T> world;
	private ResourceBundle resources;
	private DisplayMap displayMap;

	private Set<Class> gridClasses;
	private JMenu newGridMenu;

	private static int count = 0;

	/**
	 * Constructs a WorldFrame that displays the occupants of a world
	 * 
	 * @param world
	 *            the world to display
	 */
	public WorldFrame(World<T> world) {
		this.world = world;
		count++;
		resources = ResourceBundle
				.getBundle(getClass().getName() + "Resources");

		try {
			System.setProperty("sun.awt.exception.handler",
					GUIExceptionHandler.class.getName());
		} catch (SecurityException ex) {
			// will fail in an applet
		}

		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent event) {
				count--;
				if (count == 0)
					System.exit(0);
			}
		});

		displayMap = new DisplayMap();
		String title = System.getProperty("info.gridworld.gui.frametitle");
		if (title == null)
			title = resources.getString("frame.title");
		setTitle(title);
		setLocation(25, 15);

		URL appIconUrl = getClass().getResource("GridWorld.gif");
		ImageIcon appIcon = new ImageIcon(appIconUrl);
		setIconImage(appIcon.getImage());

		makeMenus();

		JPanel content = new JPanel();
		content.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
		content.setLayout(new BorderLayout());
		setContentPane(content);

		display = new GridPanel(displayMap, resources);

		KeyboardFocusManager.getCurrentKeyboardFocusManager()
				.addKeyEventDispatcher(new KeyEventDispatcher() {
					public boolean dispatchKeyEvent(KeyEvent event) {
						if (getFocusOwner() == null)
							return false;
						String text = KeyStroke.getKeyStrokeForEvent(event)
								.toString();
						final String PRESSED = "pressed ";
						int n = text.indexOf(PRESSED);
						if (n < 0)
							return false;
						// filter out modifier keys; they are neither characters
						// or actions
						if (event.getKeyChar() == KeyEvent.CHAR_UNDEFINED
								&& !event.isActionKey())
							return false;
						text = text.substring(0, n)
								+ text.substring(n + PRESSED.length());
						boolean consumed = getWorld().keyPressed(text,
								display.getCurrentLocation());
						if (consumed)
							repaint();
						return consumed;
					}
				});

		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setViewport(new PseudoInfiniteViewport(scrollPane));
		scrollPane.setViewportView(display);
		content.add(scrollPane, BorderLayout.CENTER);

		gridClasses = new TreeSet<Class>(new Comparator<Class>() {
			public int compare(Class a, Class b) {
				return a.getName().compareTo(b.getName());
			}
		});
		for (String name : world.getGridClasses())
			try {
				gridClasses.add(Class.forName(name));
			} catch (Exception ex) {
				ex.printStackTrace();
			}

		Grid<T> gr = world.getGrid();
		gridClasses.add(gr.getClass());

		makeNewGridMenu();

		control = new GUIController<T>(this, display, displayMap, resources);
		content.add(control.controlPanel(), BorderLayout.SOUTH);

		messageArea = new JTextArea(2, 35);
		messageArea.setEditable(false);
		messageArea.setFocusable(false);
		messageArea.setBackground(new Color(0xFAFAD2));
		content.add(new JScrollPane(messageArea), BorderLayout.NORTH);

		pack();
		repaint(); // to show message
		display.setGrid(gr);
	}

	public void repaint() {
		String message = getWorld().getMessage();
		if (message == null)
			message = resources.getString("message.default");
		messageArea.setText(message);
		messageArea.repaint();
		display.repaint(); // for applet
		super.repaint();
	}

	public void stop(){
		control.stop();
	}
	/**
	 * Gets the world that this frame displays
	 * 
	 * @return the world
	 */
	public World<T> getWorld() {
		return world;
	}

	/**
	 * Sets a new grid for this world. Occupants are transferred from the old
	 * world to the new.
	 * 
	 * @param newGrid
	 *            the new grid
	 */
	public void setGrid(Grid<T> newGrid) {
		Grid<T> oldGrid = world.getGrid();
		Map<Location, T> occupants = new HashMap<Location, T>();
		for (Location loc : oldGrid.getOccupiedLocations())
			occupants.put(loc, world.remove(loc));

		world.setGrid(newGrid);
		for (Location loc : occupants.keySet()) {
			if (newGrid.isValid(loc))
				world.add(loc, occupants.get(loc));
		}

		display.setGrid(newGrid);
		repaint();
	}

	/**
	 * Displays an error message
	 * 
	 * @param t
	 *            the throwable that describes the error
	 * @param resource
	 *            the resource whose .text/.title strings should be used in the
	 *            dialog
	 */
	public void showError(Throwable t, String resource) {
		String text;
		try {
			text = resources.getString(resource + ".text");
		} catch (MissingResourceException e) {
			text = resources.getString("error.text");
		}

		String title;
		try {
			title = resources.getString(resource + ".title");
		} catch (MissingResourceException e) {
			title = resources.getString("error.title");
		}

		String reason = resources.getString("error.reason");
		String message = text + "\n"
				+ MessageFormat.format(reason, new Object[] { t });

		JOptionPane.showMessageDialog(this, message, title,
				JOptionPane.ERROR_MESSAGE);
	}

	// Creates the drop-down menus on the frame.

	private JMenu makeMenu(String resource) {
		JMenu menu = new JMenu();
		configureAbstractButton(menu, resource);
		return menu;
	}

	private JMenuItem makeMenuItem(String resource, ActionListener listener) {
		JMenuItem item = new JMenuItem();
		configureMenuItem(item, resource, listener);
		return item;
	}

	private void configureMenuItem(JMenuItem item, String resource,
			ActionListener listener) {
		configureAbstractButton(item, resource);
		item.addActionListener(listener);
		try {
			String accel = resources.getString(resource + ".accel");
			String metaPrefix = "@";
			if (accel.startsWith(metaPrefix)) {
				int menuMask = getToolkit().getMenuShortcutKeyMask();
				KeyStroke key = KeyStroke.getKeyStroke(
						KeyStroke.getKeyStroke(
								accel.substring(metaPrefix.length()))
								.getKeyCode(), menuMask);
				item.setAccelerator(key);
			} else {
				item.setAccelerator(KeyStroke.getKeyStroke(accel));
			}
		} catch (MissingResourceException ex) {
			// no accelerator
		}
	}

	private void configureAbstractButton(AbstractButton button, String resource) {
		String title = resources.getString(resource);
		int i = title.indexOf('&');
		int mnemonic = 0;
		if (i >= 0) {
			mnemonic = title.charAt(i + 1);
			title = title.substring(0, i) + title.substring(i + 1);
			button.setText(title);
			button.setMnemonic(Character.toUpperCase(mnemonic));
			button.setDisplayedMnemonicIndex(i);
		} else
			button.setText(title);
	}

	private void makeMenus() {
		JMenuBar mbar = new JMenuBar();
		JMenu menu;

		menuItemsDisabledDuringRun = new ArrayList<JMenuItem>();

		mbar.add(menu = makeMenu("menu.file"));

		newGridMenu = makeMenu("menu.file.new");
		menu.add(newGridMenu);
		menuItemsDisabledDuringRun.add(newGridMenu);

		menu.add(makeMenuItem("menu.file.quit", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		}));

		mbar.add(menu = makeMenu("menu.map"));
		
		JMenuItem loadMap;
		menu.add(loadMap = makeMenuItem("menu.map.load", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				FileDialog d = new FileDialog(new Frame(), "Load map from file");
				d.setFile("*.txt");
				d.setDirectory(".");
				d.show();
				String path = d.getDirectory() + d.getFile();
				try {
					FileReader reader = new FileReader(path);
					BufferedReader br = new BufferedReader(reader);
					loadMap(br);
				} catch (FileNotFoundException e1) {
					e1.printStackTrace();
				}
			}
		}));
		menuItemsDisabledDuringRun.add(loadMap);

		mbar.add(menu = makeMenu("menu.view"));

		menu.add(makeMenuItem("menu.view.up", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.moveLocation(-1, 0);
			}
		}));
		menu.add(makeMenuItem("menu.view.down", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.moveLocation(1, 0);
			}
		}));
		menu.add(makeMenuItem("menu.view.left", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.moveLocation(0, -1);
			}
		}));
		menu.add(makeMenuItem("menu.view.right", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.moveLocation(0, 1);
			}
		}));

		JMenuItem viewEditMenu;
		menu.add(viewEditMenu = makeMenuItem("menu.view.edit",
				new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						control.editLocation();
					}
				}));
		menuItemsDisabledDuringRun.add(viewEditMenu);

		JMenuItem viewDeleteMenu;
		menu.add(viewDeleteMenu = makeMenuItem("menu.view.delete",
				new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						control.deleteLocation();
					}
				}));
		menuItemsDisabledDuringRun.add(viewDeleteMenu);

		menu.add(makeMenuItem("menu.view.zoomin", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.zoomIn();
			}
		}));

		menu.add(makeMenuItem("menu.view.zoomout", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				display.zoomOut();
			}
		}));

		mbar.add(menu = makeMenu("menu.help"));
		menu.add(makeMenuItem("menu.help.about", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				showAboutPanel();
			}
		}));
		menu.add(makeMenuItem("menu.help.help", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				showHelp();
			}
		}));
		menu.add(makeMenuItem("menu.help.license", new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				showLicense();
			}
		}));

		setRunMenuItemsEnabled(true);
		setJMenuBar(mbar);
	}

	private StringBuffer saveMap() {
		StringBuffer sBuffer = new StringBuffer("");
		Grid<T> gr = world.getGrid();
		if (display.isPannableUnbounded()) {
			sBuffer.append("unbounded\n");
		} else {
			sBuffer.append("bounded\n");
		}
		for (Location loc : gr.getOccupiedLocations())
			sBuffer.append(gr.get(loc).toString() + "\n");
		return sBuffer;
	}

	private void loadMap(BufferedReader br) {
		boolean canLoad = false;
		String str = null;
		Grid<T> gr = world.getGrid();
		for (Location loc : gr.getOccupiedLocations())
			world.remove(loc);
		repaint();
		try {
			str = br.readLine();
			if (str.equals("unbounded")) {
				if (gr.getNumCols() == -1 && gr.getNumRows() == -1) {
					canLoad=true;
				}else{
					JOptionPane.showMessageDialog(null, "Please select the unbounded grid to load this map.");
				}
			} else {
				if (gr.getNumCols() == -1 && gr.getNumRows() == -1) {
					JOptionPane.showMessageDialog(null, "Please select the bounded grid(10,10) to load this map.");
				}else{
					canLoad=true;
				}
			}
			while (((str = br.readLine()) != null) && canLoad) {
				String[] para = new String[4];
				para = str.split("\t");
				Color aColor = actorColor(para[3]);
				int direction = actorDirection(para[2]);
				Location loc = actorLocation(para[1]);
				Actor act = newActor(para[0]);
				act.setColor(aColor);
				act.setDirection(direction);
				world.add(loc, (T) act);
				
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private Color actorColor(String s) {
		String[] rgb = s.split("=");
		String r = new String(), g = new String(), b = new String();
		r += rgb[2].split(",")[0];
		g += rgb[3].split(",")[0];
		b += rgb[4].split("]")[0];
		Color c = new Color(Integer.parseInt(r), Integer.parseInt(g),
				Integer.parseInt(b));
		return c;
	}

	private int actorDirection(String s) {
		String[] dir = s.split("=");
		int d = Integer.parseInt(dir[1]);
		return d;
	}

	private Location actorLocation(String s) {
		String[] loc = s.split("=");
		String x = new String(), y = new String();
		int i = 1;
		while (loc[1].charAt(i) != ',') {
			x += loc[1].charAt(i);
			i++;
		}
		i++;
		while (loc[1].charAt(i) != ')') {
			if ((loc[1].charAt(i) >= '0') && (loc[1].charAt(i) <= '9'))
				y += loc[1].charAt(i);
			i++;
		}
		Location l = new Location(Integer.parseInt(x), Integer.parseInt(y));
		return l;
	}

	private Actor newActor(String s) {
		String act = new String();
		String temp = new String();

		for (int i = s.length() - 1; i >= 0; i--) {
			if (s.charAt(i) == '.') {
				break;
			}
			temp += s.charAt(i);
		}
		for (int j = temp.length() - 1; j >= 0; j--) {
			act += temp.charAt(j);
		}

		Actor a = new Actor();
		if (act.equals("Rock")) {
			a = new Rock();
		}
		if (act.equals("Flower")) {
			a = new Flower();
		}
		if (act.equals("MazeBug")) {
			a = new MazeBug();
		}
		return a;
	}

	private void makeNewGridMenu() {
		newGridMenu.removeAll();
		MenuMaker<T> maker = new MenuMaker<T>(this, resources, displayMap);
		maker.addConstructors(newGridMenu, gridClasses);
	}

	/**
	 * Sets the enabled status of those menu items that are disabled when
	 * running.
	 * 
	 * @param enable
	 *            true to enable the menus
	 */
	public void setRunMenuItemsEnabled(boolean enable) {
		for (JMenuItem item : menuItemsDisabledDuringRun)
			item.setEnabled(enable);
	}

	/**
	 * Brings up a simple dialog with some general information.
	 */
	private void showAboutPanel() {
		String html = MessageFormat.format(
				resources.getString("dialog.about.text"),
				new Object[] { resources.getString("version.id") });
		String[] props = { "java.version", "java.vendor", "java.home",
				"os.name", "os.arch", "os.version", "user.name", "user.home",
				"user.dir" };
		html += "<table border='1'>";
		for (String prop : props) {
			try {
				String value = System.getProperty(prop);
				html += "<tr><td>" + prop + "</td><td>" + value + "</td></tr>";
			} catch (SecurityException ex) {
				// oh well...
			}
		}
		html += "</table>";
		html = "<html>" + html + "</html>";
		JOptionPane.showMessageDialog(this, new JLabel(html),
				resources.getString("dialog.about.title"),
				JOptionPane.INFORMATION_MESSAGE);
	}

	/**
	 * Brings up a window with a scrolling text pane that display the help
	 * information.
	 */
	private void showHelp() {
		JDialog dialog = new JDialog(this,
				resources.getString("dialog.help.title"));
		final JEditorPane helpText = new JEditorPane();
		try {
			URL url = getClass().getResource("GridWorldHelp.html");

			helpText.setPage(url);
		} catch (Exception e) {
			helpText.setText(resources.getString("dialog.help.error"));
		}
		helpText.setEditable(false);
		helpText.addHyperlinkListener(new HyperlinkListener() {
			public void hyperlinkUpdate(HyperlinkEvent ev) {
				if (ev.getEventType() == HyperlinkEvent.EventType.ACTIVATED)
					try {
						helpText.setPage(ev.getURL());
					} catch (Exception ex) {
					}
			}
		});
		JScrollPane sp = new JScrollPane(helpText);
		sp.setPreferredSize(new Dimension(650, 500));
		dialog.getContentPane().add(sp);
		dialog.setLocation(getX() + getWidth() - 200, getY() + 50);
		dialog.pack();
		dialog.setVisible(true);
	}

	/**
	 * Brings up a dialog that displays the license.
	 */
	private void showLicense() {
		JDialog dialog = new JDialog(this,
				resources.getString("dialog.license.title"));
		final JEditorPane text = new JEditorPane();
		try {
			URL url = getClass().getResource("GNULicense.txt");

			text.setPage(url);
		} catch (Exception e) {
			text.setText(resources.getString("dialog.license.error"));
		}
		text.setEditable(false);
		JScrollPane sp = new JScrollPane(text);
		sp.setPreferredSize(new Dimension(650, 500));
		dialog.getContentPane().add(sp);
		dialog.setLocation(getX() + getWidth() - 200, getY() + 50);
		dialog.pack();
		dialog.setVisible(true);
	}

	/**
	 * Nested class that is registered as the handler for exceptions on the
	 * Swing event thread. The handler will put up an alert panel and dump the
	 * stack trace to the console.
	 */
	public class GUIExceptionHandler {
		public void handle(Throwable e) {
			e.printStackTrace();

			JTextArea area = new JTextArea(10, 40);
			StringWriter writer = new StringWriter();
			e.printStackTrace(new PrintWriter(writer));
			area.setText(writer.toString());
			area.setCaretPosition(0);
			String copyOption = resources.getString("dialog.error.copy");
			JOptionPane pane = new JOptionPane(new JScrollPane(area),
					JOptionPane.ERROR_MESSAGE, JOptionPane.YES_NO_OPTION, null,
					new String[] { copyOption, resources.getString("cancel") });
			pane.createDialog(WorldFrame.this, e.toString()).setVisible(true);
			if (copyOption.equals(pane.getValue())) {
				area.setSelectionStart(0);
				area.setSelectionEnd(area.getText().length());
				area.copy(); // copy to clipboard
			}
		}
	}
}
