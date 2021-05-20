import json
from typing import List, Optional
import paramiko
from dataclasses import dataclass
import select

@dataclass
class Host:
    name: str
    host: str
    user: str
    password: str
    workspace: str
    port: int = 22

class HostsStore:
    def __init__(self, hosts_file:str) -> None:
        self.hosts = self.read_hosts(hosts_file)

    def get(self, name: str) -> Optional[Host]:
        for host in self.hosts:
            if host.name == name:
                return host
        return None


    @classmethod
    def read_hosts(cls, hosts_file: str) -> List[Host]:
        with open("./hosts.json") as fr:
            hosts = json.load(fr)
        return [Host(**host) for host in hosts]



class HostControl:

    def __init__(self, host: Host) -> None:
        self.host = host
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host.host, port=host.port, username=host.user, password=host.password)

    def exec(self, cmd: str, workspace: bool = True, env: bool = True):
        print(f"H[{self.host.name}] CMD : "+cmd)
        cmd_list = []
        if workspace:
            cmd_list.append(f"cd {self.host.workspace}")
        if env:
            cmd_list.append(f"bash {self.host.workspace}/.venv/bin/activate")
        cmd_list.append(cmd)

        _, stdout, stderr = self.client.exec_command(" && ".join(cmd_list))
        for line in stderr.readlines():
            print(f"H[{self.host.name}] stderr < "+line, end="")
        return stdout.read().decode()

    def tail(self, filepath: str, n: int, BUF_SIZE: int):
        transport = self.client.get_transport()
        transport.set_keepalive(1)
        
        channel = transport.open_session()
        channel.exec_command( 'killall tail')
        channel = transport.open_session()
        cmd =f'tail -n {n} -f "{filepath}"'
        print(cmd)
        channel.exec_command(cmd)
        buf = ""
        while transport.is_active():
            try:
                rl, wl, xl = select.select([channel], [], [], 0.0)
                if len(rl) > 0:
                    new_buf = channel.recv(BUF_SIZE).decode()
                    if new_buf:
                        print(new_buf)
                        buf += new_buf
                        while True:
                            nlpos = buf.find('\n')
                            if nlpos > -1:
                                line = buf[:nlpos+1]
                                
                                yield line
                                buf = buf[nlpos+1:]
                            else:
                                break
            except Exception as e:
                print("stopped: " + e)

    def __del__(self):
        self.client.close()
        print("ssh closed")