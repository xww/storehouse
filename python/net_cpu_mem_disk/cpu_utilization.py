#!/usr/bin/python
# -*- coding:utf8 -*-
import time
import os
 
def cpu_rate():
    #import ipdb;ipdb.set_trace()
    def cpu_r():
        f = open("/proc/stat","r")
        for f_line in f:
            break
        f.close()
        f_line = f_line.split(" ")
        f_line_a=[]
        for i in f_line:
            if i.isdigit():
                i=int(i)
                f_line_a.append(i)
        total = sum(f_line_a)
        idle = f_line_a[3]
        return total,idle
 
    total_a,idle_a=cpu_r()
    time.sleep(2)
    total_b,idle_b=cpu_r()
 
    sys_idle = idle_b - idle_a
    sys_total = total_b - total_a
    sys_us = sys_total - sys_idle
 
    cpu_a = (float(sys_us)/sys_total)*100
    return cpu_a

print cpu_rate()

def cpu_util_rate():
    def static_cpu_time(line):
        cpu_total_time = 0
        for item in line:
            if item.isdigit():
                cpu_total_time += int(item)
        idle_time = int(line[4])
        return [cpu_total_time - idle_time, cpu_total_time]
    
    def get_cpu_data():
        data = {}
        processors = int(os.popen('cat /proc/cpuinfo | grep "processor" | wc -l').read()[:-1])
        with open("/proc/stat","r") as f:            
            for line in f.readlines()[0: processors+1]:
                line = line[:-1].split()
                result = static_cpu_time(line)
                data[line[0]] = result
        return data

    result1 = get_cpu_data()
    time.sleep(2)
    result2 = get_cpu_data()

    result = {}
    for k in result1:
        result[k] = (float(result2[k][0] - result1[k][0])/(result2[k][1] - result1[k][1]))*100
    return result   

print cpu_util_rate()
