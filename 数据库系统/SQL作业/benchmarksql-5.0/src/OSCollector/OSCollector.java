/*
 * OSCollector.java
 *
 * Copyright (C) 2016, Denis Lussier
 * Copyright (C) 2016, Jan Wieck
 *
 */

import org.apache.log4j.*;

import java.lang.*;
import java.io.*;
import java.util.*;

public class OSCollector
{
    private String		script;
    private int			interval;
    private String		sshAddress;
    private String		devices;
    private File		outputDir;
    private Logger		log;

    private CollectData		collector = null;
    private Thread		collectorThread = null;
    private boolean		endCollection = false;
    private Process		collProc;

    private BufferedWriter	resultCSVs[];

    public OSCollector(String script, int runID, int interval,
    		       String sshAddress, String devices, File outputDir,
		       Logger log)
    {
    	List<String>	cmdLine = new ArrayList<String>();
	String		deviceNames[];

    	this.script	= script;
	this.interval	= interval;
	this.sshAddress	= sshAddress;
	this.devices	= devices;
	this.outputDir	= outputDir;
	this.log	= log;

	if (sshAddress != null)
	{
	    cmdLine.add("ssh");
	    // cmdLine.add("-t");
	    cmdLine.add(sshAddress);
	}
	cmdLine.add("python");
	cmdLine.add("-");
	cmdLine.add(Integer.toString(runID));
	cmdLine.add(Integer.toString(interval));
	if (devices != null)
	    deviceNames = devices.split("[ \t]+");
	else
	    deviceNames = new String[0];

	try
	{
	    resultCSVs = new BufferedWriter[deviceNames.length + 1];
	    resultCSVs[0] = new BufferedWriter(new FileWriter(
		    new File(outputDir, "sys_info.csv")));
	    for (int i = 0; i < deviceNames.length; i++)
	    {
		cmdLine.add(deviceNames[i]);
		resultCSVs[i + 1] = new BufferedWriter(new FileWriter(
			new File(outputDir, deviceNames[i] + ".csv")));
	    }
	}
	catch (Exception e)
	{
	    log.error("OSCollector, " + e.getMessage());
	    System.exit(1);
	}

	try
	{
	    ProcessBuilder pb = new ProcessBuilder(cmdLine);
	    pb.redirectError(ProcessBuilder.Redirect.INHERIT);

	    collProc = pb.start();

	    BufferedReader scriptReader = new BufferedReader(new FileReader(script));
	    BufferedWriter scriptWriter = new BufferedWriter(
	    		new OutputStreamWriter(collProc.getOutputStream()));
	    String line;
	    while ((line = scriptReader.readLine()) != null)
	    {
		scriptWriter.write(line);
		scriptWriter.newLine();
	    }
	    scriptWriter.close();
	    scriptReader.close();
	}
	catch (Exception e)
	{
	    log.error("OSCollector " + e.getMessage());
	    e.printStackTrace();
	    System.exit(1);
	}

	collector = new CollectData(this);
	collectorThread = new Thread(this.collector);
	collectorThread.start();
    }

    public void stop()
    {
    	endCollection = true;
	try
	{
	    collectorThread.join();
	}
	catch (InterruptedException ie)
	{
	    log.error("OSCollector, " + ie.getMessage());
	    return;
	}
    }

    private class CollectData implements Runnable
    {
    	private OSCollector	parent;

    	public CollectData(OSCollector parent)
	{
	    this.parent = parent;
	}

	public void run()
	{
	    BufferedReader	osData;
	    String		line;
	    int			resultIdx = 0;

	    osData = new BufferedReader(new InputStreamReader(
	    		parent.collProc.getInputStream()));

	    while (!endCollection || resultIdx != 0)
	    {
		try
		{
		    line = osData.readLine();
		    if (line == null)
		    {
		    	log.error("OSCollector, unexpected EOF " +
				  "while reading from external " +
				  "helper process");
		    	break;
		    }
		    parent.resultCSVs[resultIdx].write(line);
		    parent.resultCSVs[resultIdx].newLine();
		    parent.resultCSVs[resultIdx].flush();
		    if (++resultIdx >= parent.resultCSVs.length)
		    	resultIdx = 0;
		}
		catch (Exception e)
		{
		    log.error("OSCollector, " + e.getMessage());
		    break;
		}
	    }

	    try
	    {
		osData.close();
		for (int i = 0; i < parent.resultCSVs.length; i++)
		    parent.resultCSVs[i].close();
	    }
	    catch (Exception e)
	    {
	    	log.error("OSCollector, " + e.getMessage());
	    }
	}
    }
}


