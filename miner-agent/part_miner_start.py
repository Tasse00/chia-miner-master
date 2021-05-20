#!.venv/bin/python

# 启动　part miner
# - 检查是否已经在运行
# - 后台启动 part miner，并记录pid

import os
import subprocess
import click
import psutil
import yaml

from utils.cmdutil import ret
from utils.diskutil import get_hdds



@click.command()
def start():
    config_filepath = os.path.join(os.path.dirname(__file__), "miner", "config.yaml",)
    if not os.path.exists(config_filepath):
        return ret(False, "miner not init")
    bin_filepath = os.path.join(os.path.dirname(__file__), "resources", "hpool-miner", "hpool-miner-chia")

    subprocess.Popen(["nohup", bin_filepath, "-config", config_filepath, ">/dev/null", "2>&1", "&"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn = os.setsid)

    ret(True, "ok")


if __name__ == "__main__":
    start()

