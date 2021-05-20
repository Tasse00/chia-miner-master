#!.venv/bin/python
# 启动　part miner
# - 杀死miner进程(若存在)


import os
import click
import psutil
import yaml
import os
import signal

from utils.cmdutil import ret
from utils.diskutil import get_hdds



@click.command()
def stop():
    pids = []
    for p in psutil.process_iter():
        if p.name() == "hpool-miner-chia":
            pids.append(str(p.pid))
            os.kill(p.pid, signal.SIGKILL)


    ret(True, f"killed: {','.join(pids)}")


if __name__ == "__main__":
    stop()

