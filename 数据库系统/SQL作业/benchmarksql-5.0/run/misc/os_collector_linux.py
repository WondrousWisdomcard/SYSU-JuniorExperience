#!/usr/bin/env python
# ----------------------------------------------------------------------
# os_collector_linux.py -
#
#   Script used to collect OS level resource utilization data like
#   CPU usage and disk IO.
#
#   This code is used in the jTPCCOSCollect class. It is launched as
#   a separate process, possibly via ssh(1) on the remote database
#   server. The ability of Python to receive a script to execute on
#   stdin allows us to execute this script via ssh(1) on the database
#   server without installing any programs/scripts there.
#
#   The command line arguments for this script are the runID, the
#   interval in seconds at which to collect information and a variable
#   number of devices in the form "blk_<devname>" "net_<devname>",
#   for example "blk_sda" for the first SCSI disk or "net_eth0".
#
#   The output on stdout is one line for CPU/VM info, followed by a
#   line for each of the specified devices in CSV format. The first
#   set of lines are the CSV headers. The output is prefixed with the
#   runID, elapsed_ms and for the devices the blk_ or net_ name that
#   was specified on the command line. This format makes it easy to
#   load the data into a result database where it can be analyzed
#   together with the BenchmarkSQL per transaction results and compared
#   to other benchmark runs.
#
#   It is the caller's responsibility to split the output lines into
#   separate result CSV files.
# ----------------------------------------------------------------------

import errno
import math
import os
import sys
import time

# ----
# main
# ----
def main(argv):
    global  deviceFDs
    global  lastDeviceData

    # ----
    # Get the runID and collection interval from the command line
    # ----
    runID = (int)(argv[0])
    interval = (float)(argv[1])

    # ----
    # Our start time is now. Since most of the information is deltas
    # we can only produce the first data after the first interval.
    # ----
    startTime = time.time();
    nextDue = startTime + interval

    # ----
    # Initialize CPU and vmstat collection and output the CSV header.
    # ----
    sysInfo = ['run', 'elapsed', ]
    sysInfo += initSystemUsage()
    print ",".join([str(x) for x in sysInfo])

    # ----
    # Get all the devices from the command line.
    # ----
    devices = []
    deviceFDs = {}
    lastDeviceData = {}
    for dev in argv[2:]:
        if dev.startswith('blk_'):
            devices.append(dev)
        elif dev.startswith('net_'):
            devices.append(dev)
        else:
            raise Exception("unknown device type '" + dev + "'")

    # ----
    # Initialize usage collection per device depending on the type.
    # Output all the headers in the order, the devices are given.
    # ----
    for dev in devices:
        if dev.startswith('blk_'):
            devInfo = ['run', 'elapsed', 'device', ]
            devInfo += initBlockDevice(dev)
            print ",".join([str(x) for x in devInfo])
        elif dev.startswith('net_'):
            devInfo = ['run', 'elapsed', 'device', ]
            devInfo += initNetDevice(dev)
            print ",".join([str(x) for x in devInfo])

    # ----
    # Flush all header lines.
    # ----
    sys.stdout.flush()

    try:
        while True:
            # ----
            # Wait until our next collection interval and calculate the
            # elapsed time in milliseconds.
            # ----
            now = time.time()
            if nextDue > now:
                time.sleep(nextDue - now)
            elapsed = (int)((nextDue - startTime) * 1000.0)

            # ----
            # Collect CPU and vmstat information.
            # ----
            sysInfo = [runID, elapsed, ]
            sysInfo += getSystemUsage()
            print ",".join([str(x) for x in sysInfo])

            # ----
            # Collect all device utilization data.
            # ----
            for dev in devices:
                if dev.startswith('blk_'):
                    devInfo = [runID, elapsed, dev, ]
                    devInfo += getBlockUsage(dev, interval)
                    print ",".join([str(x) for x in devInfo])
                elif dev.startswith('net_'):
                    devInfo = [runID, elapsed, dev, ]
                    devInfo += getNetUsage(dev, interval)
                    print ",".join([str(x) for x in devInfo])

            # ----
            # Bump the time when we are next due.
            # ----
            nextDue += interval

            sys.stdout.flush()

    # ----
    # Running on the command line for test purposes?
    # ----
    except KeyboardInterrupt:
        print ""
        return 0

    # ----
    # The OSCollector class will just close our stdout on the other
    # side, so this is expected.
    # ----
    except IOError as e:
        if e.errno == errno.EPIPE:
            return 0
        else:
            raise e

def initSystemUsage():
    global  procStatFD
    global  procVMStatFD
    global  lastStatData
    global  lastVMStatData

    procStatFD = open("/proc/stat", "r", buffering = 0)
    for line in procStatFD:
        line = line.split()
        if line[0] == "cpu":
            lastStatData = [int(x) for x in line[1:]]
            break
    if len(lastStatData) != 10:
        raise Exception("cpu line in /proc/stat too short");

    procVMStatFD = open("/proc/vmstat", "r", buffering = 0)
    lastVMStatData = {}
    for line in procVMStatFD:
        line = line.split()
        if line[0] in ['nr_dirty', ]:
            lastVMStatData['vm_' + line[0]] = int(line[1])
    if len(lastVMStatData.keys()) != 1:
        raise Exception("not all elements found in /proc/vmstat")
        
    return [
            'cpu_user', 'cpu_nice', 'cpu_system',
            'cpu_idle', 'cpu_iowait', 'cpu_irq',
            'cpu_softirq', 'cpu_steal',
            'cpu_guest', 'cpu_guest_nice',
            'vm_nr_dirty',
        ]


def getSystemUsage():
    global  procStatFD
    global  procVMStatFD
    global  lastStatData
    global  lastVMStatData

    procStatFD.seek(0, 0);
    for line in procStatFD:
        line = line.split()
        if line[0] != "cpu":
            continue
        statData = [int(x) for x in line[1:]]
        deltaTotal = (float)(sum(statData) - sum(lastStatData))
        if deltaTotal == 0:
            result = [0.0 for x in statData]
        else:
            result = []
            for old, new in zip(lastStatData, statData):
                result.append((float)(new - old) / deltaTotal)
        procStatLast = statData
        break

    procVMStatFD.seek(0, 0)
    newVMStatData = {}
    for line in procVMStatFD:
        line = line.split()
        if line[0] in ['nr_dirty', ]:
            newVMStatData['vm_' + line[0]] = int(line[1])
    
    for key in ['vm_nr_dirty', ]:
        result.append(newVMStatData[key])

    return result


def initBlockDevice(dev):
    global  deviceFDs
    global  lastDeviceData

    devPath = os.path.join("/sys/block", dev[4:], "stat")
    deviceFDs[dev] = open(devPath, "r", buffering = 0)
    line = deviceFDs[dev].readline().split()

    newData = []
    for idx, mult in [
                (0, 1.0), (1, 1.0), (2, 0.5),
                (4, 1.0), (5, 1.0), (6, 0.5),
            ]:
        newData.append((int)(line[idx]))
    lastDeviceData[dev] = newData

    return ['rdiops', 'rdmerges', 'rdkbps', 'wriops', 'wrmerges', 'wrkbps', ]


def getBlockUsage(dev, interval):
    global  deviceFDs

    deviceFDs[dev].seek(0, 0)
    line = deviceFDs[dev].readline().split()

    oldData = lastDeviceData[dev]
    newData = []
    result = []
    ridx = 0
    for idx, mult in [
                (0, 1.0), (1, 1.0), (2, 0.5),
                (4, 1.0), (5, 1.0), (6, 0.5),
            ]:
        newData.append((int)(line[idx]))
        result.append((float)(newData[ridx] - oldData[ridx]) * mult / interval)
        ridx += 1
    lastDeviceData[dev] = newData
    return result

def initNetDevice(dev):
    global  deviceFDs
    global  lastDeviceData

    devPath = os.path.join("/sys/class/net", dev[4:], "statistics")
    deviceData = []
    for fname in ['rx_packets', 'rx_bytes', 'tx_packets', 'tx_bytes', ]:
        key = dev + "." + fname
        deviceFDs[key] = open(os.path.join(devPath, fname),
                              "r", buffering = 0)
        deviceData.append((int)(deviceFDs[key].read()))

    lastDeviceData[dev] = deviceData

    return ['rxpktsps', 'rxkbps', 'txpktsps', 'txkbps', ]


def getNetUsage(dev, interval):
    global  deviceFDs
    global  lastDeviceData

    oldData = lastDeviceData[dev]
    newData = []
    for fname in ['rx_packets', 'rx_bytes', 'tx_packets', 'tx_bytes', ]:
        key = dev + "." + fname
        deviceFDs[key].seek(0, 0)
        newData.append((int)(deviceFDs[key].read()))

    result = [
            (float)(newData[0] - oldData[0]) / interval,
            (float)(newData[1] - oldData[1]) / interval / 1024.0,
            (float)(newData[2] - oldData[2]) / interval,
            (float)(newData[3] - oldData[3]) / interval / 1024.0,
        ]
    lastDeviceData[dev] = newData
    return result


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
