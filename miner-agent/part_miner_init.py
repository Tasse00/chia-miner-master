#!.venv/bin/python

# 初始化config文件
# - 建立各个part的miner目录
# - 设置 minerName , paths

import os
import click
import yaml

from utils.cmdutil import ret
from utils.diskutil import get_hdds


@click.command()
@click.option("--miner-name", required=True)
def init(miner_name: str):
    config_filepath = os.path.join(os.path.dirname(__file__), "resources", "hpool-miner", "config.yaml")

    miner_dir = os.path.join(os.path.dirname(__file__), "miner")
    os.makedirs(miner_dir, exist_ok=True)

    part_config_file = os.path.join(miner_dir, "config.yaml")

    data = yaml.load(open(config_filepath), Loader=yaml.FullLoader)
    data['minerName'] = miner_name

    plots_dirs = []
    hdds = get_hdds()
    for hdd in hdds:
        part_plot_dir = os.path.join(hdd['mountpoint'], "plots")
        os.makedirs(part_plot_dir, exist_ok=True)
        plots_dirs.append(part_plot_dir)
        

    data['path'] = plots_dirs
    data['log']['path'] = os.path.join(miner_dir, "logs")

    yaml.dump(data, open(part_config_file, 'w'))
    ret(True, "ok")

if __name__ == "__main__":

    init()