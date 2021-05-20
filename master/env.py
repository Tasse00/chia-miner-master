import os
import paramiko
import click
import tempfile
import zipfile
import json


from master.utils.hostutil import HostControl, Host, HostsStore

def clean_miner_agent_workspace(host: Host):
    """删除miner-agent的workspace目录并重建"""

    hc = HostControl(host)
    hc.exec(f"rm -rf {host.workspace}", workspace=False, env=False)
    hc.exec(f"mkdir {host.workspace}", workspace=False, env=False)

def send_miner_agent_zip(miner_agent_dir: str, host: Host):
    hostname = host.host
    port = host.port
    username = host.user
    password = host.password
    target_workspace = host.workspace
    
    # 压缩
    with tempfile.NamedTemporaryFile(mode='wb', suffix=".zip") as tmp:
        
        agent_zip=zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)

        for d,_,fs in os.walk(miner_agent_dir):
            for f in fs:
                abs_f = os.path.join(d, f)
                rel_f = os.path.relpath(abs_f, miner_agent_dir)
                agent_zip.write(abs_f, rel_f)
        agent_zip.close()

        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(tmp.name, os.path.join(target_workspace, "miner-agent.zip"))
        transport.close()

def install_miner_agent(host: Host):

    # 0 clean workspace
    # 1 unzip
    # 2 install

    hc = HostControl(host)
    hc.exec("unzip -o miner-agent.zip", env=False)
    hc.exec("bash install/init-venv.sh", env=False)


## 检查状态: 是否已安装
# agent check env -h test
## 安装
# agent install env -h test
## 查看磁盘
# agent list disks -h test



@click.group()
def env():
    pass

@env.command("check")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def env_check(host: str, hosts_file: str):
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    hc = HostControl(h)
    try:
        res_json = json.loads(hc.exec("./check_env.py"))
    except Exception as e:
        click.echo("Env not ready: "+str(e))
    else:
        print(res_json)

@env.command("clean")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
def env_clean(host: str, hosts_file: str):
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    click.echo("cleaning workspace...")
    clean_miner_agent_workspace(h)


@env.command("install")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
@click.option("--miner-agent-dir", default="./miner-agent")
def env_install(host: str, hosts_file: str, miner_agent_dir: str):
    hs = HostsStore(hosts_file)
    h = hs.get(host)
    if h is None:
        click.echo("invalid host")
        return
    click.echo("cleaning workspace...")
    clean_miner_agent_workspace(h)
    click.echo("zip and transporting...")
    send_miner_agent_zip(miner_agent_dir, h)
    click.echo("installing...")
    install_miner_agent(h)
    click.echo("ok")

