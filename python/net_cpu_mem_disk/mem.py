#!/usr/bin/env python
import time
import os

def get_mem_data():
    #import ipdb;ipdb.set_trace()
    mem_info = os.popen('free').read().split("\n")[1].split()
    #mem_info=mem_info.split()
    # mem_free = free + buffers + cached
    return 1.0 - float(int(mem_info[3]) + int(mem_info[5]) + int(mem_info[6]))/int(mem_info[1])


print get_mem_data()
