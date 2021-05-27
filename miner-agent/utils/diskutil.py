import psutil
import os
from itertools import groupby

def get_mountpoint(part: str):
    for p in psutil.disk_partitions():
        if p.device == part:
            return p.mountpoint


def get_hdds(ignore_root: bool = True):

    # 找到机械盘
    output = os.popen('lsblk -d -o name,rota | grep -v loop | grep -v " 0" | sed 1d')
    result = output.read()
    devices = [line.split(" ")[0] for line in result.splitlines()]


    # 从分区找到磁盘
    def get_device_disk(device: str):
        parts = [''.join(list(g)) for k, g in groupby(device, key=lambda x: x.isdigit())]
        if len(parts)==1:
            return os.path.basename(parts[0])
        else:
            first = "".join(parts[:-1])
            second = "".join(parts[-1:])
            return os.path.basename(first)

    disks = psutil.disk_partitions()
    # 找到机械盘下的所有分区
    valid_disks = []

    for disk in disks:
        if disk.fstype in ['squashfs']:
            continue
        if ignore_root and disk.mountpoint == '/':
            continue
        if disk.mountpoint.startswith("/boot"):
            continue
        if get_device_disk(disk.device) in devices:
            valid_disks.append(disk)

    json_data = []
    for d in valid_disks:
        
        usage = psutil.disk_usage(d.mountpoint)
        # print(d)
        # print(usage)
        json_data.append({
            "part": d.device,
            "device": get_device_disk(d.device),
            "fstype": d.fstype,
            "mountpoint": d.mountpoint,
            # "opts": d.opts,
            "total": usage.total,
            "used": usage.used,
        })
    return json_data

        