#!/usr/bin/env python
import time

VALID_NIC_NAME_PREFIX = ['bond', 'eth', 'em']
NET_TASK_INTERVAL = 2
def get_net_data():
    net = {}
    with open("/proc/net/dev") as f:
        for line in f.readlines()[2:]:
            line = line[:-1].split()
            for nic_name_prefix in VALID_NIC_NAME_PREFIX:
                if nic_name_prefix in line[0]:
                    net[line[0]] = [line[1], line[9]]
    print net
    return net


def net_rate_static():
    result1 = get_net_data()
    time.sleep(NET_TASK_INTERVAL)
    result2 = get_net_data()

    result = {}
    for key in result1:
        result[key] = [(int(result2[key][0]) - int(result1[key][0]))/NET_TASK_INTERVAL, 
                       (int(result2[key][1]) - int(result1[key][1]))/NET_TASK_INTERVAL]
    return result
                    
print net_rate_static()
