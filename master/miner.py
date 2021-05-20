

# === mine commands ===

import json
from master.utils.hostutil import HostControl, HostsStore
import click
import os
import terminaltables


@click.group()
def miner():
    pass

@miner.command("status")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def mine_status(host: str, hosts_file: str):
    """查看所有part的mining状态"""
    """
    -------------------------------------------------------
    | host | part | total | used  | plots | init | mining |
    -------------------------------------------------------
    | 005  | sda1 | 1.82T | 1.04T | 0.2T  |  ok  |   yes  |
    -------------------------------------------------------
    """
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    
    hc = HostControl(h)
    _res = hc.exec(f"./part_miner_status.py")
    res = json.loads(_res)
   
    if res['success']:
        dat = res['message']
        
        miner_pid_msg = f"Miner Pid: {','.join(dat['pids']) if dat['pids'] else 'not mining!'}"
        click.echo("-"*len(miner_pid_msg))
        click.echo(miner_pid_msg)
        
        hdds = dat['hdds']
        for hdd in hdds:
            hdd['total'] = f"{round(hdd['total']/1024/1024/1024/1024, 2)}T"
            hdd['used'] = f"{round(hdd['used']/1024/1024/1024/1024, 2)}T"
            hdd['plots_size'] = f"{round(hdd['plots_size']/1024/1024/1024/1024, 2)}T"
        rows = [
            list(hdds[0].keys())
        ]
        for hdd in hdds:
            row = []
            for col in rows[0]:
                row.append(hdd[col]) 
            rows.append(row)

        table = terminaltables.AsciiTable(rows)
        click.echo(table.table)




@miner.command("init")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def miner_init(host: str, hosts_file: str):
    """创建part miner的config"""
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    
    hc = HostControl(h)
    _res = hc.exec(f"./part_miner_init.py --miner-name={h.name}")
    res = json.loads(_res)
    if res['success']:
        click.echo("ok")
    else:
        click.echo("Failed: "+res['message'])


@miner.command("start")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def miner_start(host: str, hosts_file: str):
    """创建part miner的config"""
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    
    hc = HostControl(h)
    _res = hc.exec(f"./part_miner_start.py")
    res = json.loads(_res)
    if res['success']:
        click.echo("ok")
    else:
        click.echo("Failed: "+res['message'])
    


@miner.command("stop")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def miner_stop(host: str, hosts_file: str):
    """创建part miner的config"""
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    
    hc = HostControl(h)
    _res = hc.exec(f"./part_miner_stop.py")
    res = json.loads(_res)
    if res['success']:
        click.echo(""+res['message'])
    else:
        click.echo("Failed: "+res['message'])

@miner.command("log")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
@click.option("--lines", default=10, type=int)
def miner_log(host: str, hosts_file: str, lines: int):
    """查看日志"""
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    
    hc = HostControl(h)
    for line in hc.exec(f'tail {os.path.join(h.workspace, "miner", "logs", "miner.log")} -n {lines}'):
        print(line, end="")
    