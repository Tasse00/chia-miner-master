import click
import json
import terminaltables

from master.utils.hostutil import HostsStore, HostControl

@click.group()
def device():
    pass


@device.command("hdds")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def hdds(host: str, hosts_file: str):
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    hc = HostControl(h)
    res = hc.exec(f"./get_hdds.py")
    hdds = json.loads(res)

    for hdd in hdds:
        hdd['total'] = f"{round(hdd['total']/1024/1024/1024/1024, 2)}T"
        hdd['used'] = f"{round(hdd['used']/1024/1024/1024/1024, 2)}T"

    if not hdds:
        click.echo("no hdds")
        return
    
    rows = [
        list(hdds[0].keys())
    ]
    for hdd in hdds:
        row = []
        for col in rows[0]:
           row.append(hdd[col]) 
        rows.append(row)

    table = terminaltables.AsciiTable(rows)
    print(table.table)
    return hdds
