

# === mine commands ===

import json
from typing import Optional
from master.utils.hostutil import HostControl, HostsStore
import click
import os
import terminaltables


@click.group()
def miner():
    pass

@miner.command("status")
@click.option("--host")
@click.option("--hosts-file", default="./hosts.json")
def mine_status(host: Optional[str], hosts_file: str):
    """查看所有part的mining状态"""
    """
    -------------------------------------------------------
    | host | part | total | used  | plots | init | mining |
    -------------------------------------------------------
    | 005  | sda1 | 1.82T | 1.04T | 0.2T  |  ok  |   yes  |
    -------------------------------------------------------
    """
    hs = HostsStore(hosts_file)

    h_list = []

    if host != None:
        h = hs.get(host)
        if h is None:
            click.echo("invalid host")
            return
        h_list = [h]
    else:
        h_list = hs.hosts

    def fetch_results():
        for h in h_list:
            # click.echo(f"\n\n# {h.name} at {h.host}")
            hc = HostControl(h)
            try:
                _res = hc.exec(f"./part_miner_status.py")
                res = json.loads(_res)
                info = {}
                if res['success']:
                    dat = res['message']
                    info.update(dat)

                    # miner_pid_msg = f"Miner Pid: {','.join(dat['pids']) if dat['pids'] else 'not mining!'}"
                    # click.echo("-"*len(miner_pid_msg))
                    # click.echo(miner_pid_msg)

                    hdds = dat['hdds']
                    for hdd in hdds:
                        hdd['nice_total'] = f"{round(hdd['total']/1024/1024/1024/1024, 2)}T"
                        hdd['nice_used'] = f"{round(hdd['used']/1024/1024/1024/1024, 2)}T"
                        hdd['nice_plots_size'] = f"{round(hdd['plots_size']/1024/1024/1024/1024, 2)}T"

                    yield {
                        "host": h,
                        "data": dat
                    }

                    # rows = [
                    #     list(hdds[0].keys())
                    # ]
                    # for hdd in hdds:
                    #     row = []
                    #     for col in rows[0]:
                    #         row.append(hdd[col])
                    #     rows.append(row)

                    # table = terminaltables.AsciiTable(rows)
                    # click.echo(table.table)
            except Exception as e:
                click.echo(f" - ERROR: {e}")
                yield {
                    "host": h,
                    "data": {}
                }

    fields = [
        ["Host", lambda h,d,hdd: h.name],
        ["IP", lambda h,d,hdd: h.host],
        ["Pid", lambda h,d,hdd: ",".join(d['pids'])],
        ["Part", lambda h,d,hdd: hdd['part']],
        ["MountPoint", lambda h,d,hdd: hdd['mountpoint']],
        ["Total", lambda h,d,hdd: hdd['nice_total']],
        ["Used", lambda h,d,hdd: hdd['nice_used']],
        ["PlotSize", lambda h,d,hdd: hdd['nice_plots_size']],
        ["PlotDir", lambda h,d,hdd: hdd['plots_dir']],
        ["Configed", lambda h,d,hdd: hdd['configed']],
        ["Rest", lambda h,d,hdd: f"{100 - round((hdd['used'] / hdd['total']*100), 2)}%"],
    ]
    rows = [
        [ f[0] for f in fields]
    ]
    totals = []
    for result in fetch_results():
        h = result['host']
        dat = result['data']
        
        for hdd in dat['hdds']:
            row = []
            for f in fields:
                try:
                    v = f[1](h, dat, hdd)
                except:
                    v = ''
                row.append(v)
            rows.append(row)
        
        # 插入间隔符
        # rows.append(['']*len(fields))
        totals.append({"host": h.name, "plots_size": sum([hdd['plots_size'] for hdd in dat['hdds']])})
    # rows = rows[:-1]

    table = terminaltables.AsciiTable(rows)
    print(table.table)
    click.echo("   ".join([ f"[{t['host']}: {round(t['plots_size']/1024/1024/1024/1024, 2)}T]" for t in totals]))
    click.echo(f"Total: {round(sum([t['plots_size'] for t in totals])/1024/1024/1024/1024, 2)}T")


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
