import psutil
import signal
import threading
import time

TASK_INTERVAL = 2
IS_EXIST = False

def get_disk_io():
    def _innner():
        a=psutil.disk_io_counters(perdisk=False)
        time.sleep(TASK_INTERVAL)
        b=psutil.disk_io_counters()
        read_iops = (b.read_count - a.read_count)/TASK_INTERVAL
        write_iops = (b.write_count - a.write_count)/TASK_INTERVAL
        read_rate = (b.read_bytes - a.read_bytes)/TASK_INTERVAL/1024/1024
        write_rate = (b.write_bytes - a.write_bytes)/TASK_INTERVAL/1024/1024
        #print 'iops',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), read_iops,write_iops,read_rate,write_rate
    while not IS_EXIST:
        #print 'now is: ', time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        threading.Thread(target=_innner).start()
        time.sleep(TASK_INTERVAL)
    

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


def get_mem_usage():
    return psutil.phymem_usage().percent


def get_cpu_rate():
    return psutil.cpu_percent(percpu=False)


def get_net_io():
    a=psutil.net_io_counters(pernic=False)
    time.sleep(4)
    b=psutil.net_io_counters(pernic=False)
    return (b.bytes_sent-a.bytes_sent)/4, (b.bytes_recv-a.bytes_recv)/4

def main():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    threadpool=[]
    disk_thread = threading.Thread(target=get_disk_io);disk_thread.setDaemon(True);threadpool.append(disk_thread)
    mem_thread = threading.Thread(target=get_mem_usage);mem_thread.setDaemon(True);threadpool.append(mem_thread)
    cpu_thread = threading.Thread(target=get_cpu_rate);cpu_thread.setDaemon(True);threadpool.append(cpu_thread)
    net_thread = threading.Thread(target=get_net_io);net_thread.setDaemon(True);threadpool.append(net_thread)
    for thread in threadpool:
        thread.start()
    #for th in threadpool: join method will result in  signal ctrl+c capture fail
    #    threading.Thread.join(th)
    while True:
        alive = False
        for thread in threadpool:
            alive = alive or thread.isAlive()
        if not alive:
            break;
    print "main exit"

def handler(signum, frame):
    global IS_EXIST
    IS_EXIST = True
    print "receive a signal %d, is_exit = %d"%(signum, IS_EXIST)

if __name__ == '__main__':
    main()


#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
