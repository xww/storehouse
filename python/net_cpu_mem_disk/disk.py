#!/usr/bin/env python
import time
import os

def get_disk_partitions(all=False):
    """Return all mountd partitions as a nameduple.
    If all == False return phyisical partitions only.
    """
    disks = []
    phydevs = []
    f = open("/proc/filesystems", "r")
    for line in f:
        if not line.startswith("nodev"):
            phydevs.append(line.strip())

    retlist = []
    f = open('/etc/mtab', "r")
    for line in f:
        if not all and line.startswith('none'):
            continue
        fields = line.split()
        device = fields[0]
        mountpoint = fields[1]
        fstype = fields[2]
        if not all and fstype not in phydevs:
            continue
        if device == 'none':
            device = ''
        disks.append({'divice': device, 'mountpoint': mountpoint, 'fstype': fstype})
    return disks

def get_disk_usage_old():
    disks = get_disk_partitions()
    for disk in disks:
        hd = {}
        disk_info = os.statvfs(disk['mountpoint'])        
        hd['available'] = disk.f_bsize * disk.f_bavail/1024/1024
        hd['capacity'] = disk.f_bsize * disk.f_blocks/1024/1024
        hd['used'] =(disk.f_blocks-disk.f_bfree)*disk.f_frsize/1024/1024
        print hd

#print get_disk_partitions()
#print get_disk_usage()

import psutil

timeaa=4
def get_disk_io():
    a=psutil.disk_io_counters()
    time.sleep(timeaa)
    b=psutil.disk_io_counters()
    read_iops = (b.read_count - a.read_count)/timeaa
    write_iops = (b.write_count - a.write_count)/timeaa
    read_rate = (b.read_bytes - a.read_bytes)/timeaa/1024/1024
    write_rate = (b.write_bytes - a.write_bytes)/timeaa/1024/1024
    print read_iops,write_iops,read_rate,write_rate


print get_disk_io()

def get_disk_usage():
    partitions = psutil.disk_partitions()
    disk_partitions_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_partitions_info.append({'device': partition.device, 'mountpoint': partition.mountpoint, 
                                     'fstype': partition.fstype, 'opts': partition.opts, 
                                     'usage':{'total': str(usage.total/1024/1024)+ 'MB', 
                                              'used': str(usage.used/1024/1024)+ 'MB', 
                                              'free':str(usage.free/1024/1024)+ 'MB'}                                                                
                                     })
    return disk_partitions_info

print get_disk_usage()







