#!.venv/bin/python

# 获取 part miner 的状态
# - 是否在工作
# - plots数量

import os
from os.path import getsize, join
import click
import yaml
import psutil

from utils.cmdutil import ret
from utils.diskutil import get_hdds

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


@click.command()
def status():
    config_filepath = os.path.join(os.path.dirname(__file__), "miner", "config.yaml",)

    pids = []
    for p in psutil.process_iter():
        if p.name() == "hpool-miner-chia":
            pids.append(str(p.pid))

    config = None
    if os.path.exists(config_filepath):
        config = yaml.load(open(config_filepath, 'r'), Loader=yaml.FullLoader)


    hdds = get_hdds()
    for hdd in hdds:
        plot_dir = os.path.join(hdd['mountpoint'], 'plots')
        hdd['plots_dir'] = plot_dir
        hdd['plots_size'] = getdirsize(plot_dir)
        hdd['configed'] = (plot_dir in config['path']) if config else 'Not Init!'
    

    ret(True, {
        "pids": pids,
        "hdds": hdds,
        "config": config,
    })


if __name__ == "__main__":
    status()
