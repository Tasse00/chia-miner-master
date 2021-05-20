import click

@click.group()
def plots():
    pass


@plots.command("send")
@click.option("--host", required=True)
@click.option("--hosts-file", default="./hosts.json")
@click.option("--src-file", required=True)
@click.option("--remove-after-finished", default=False, type=bool)
@click.option("--trans-server", default=True)
def send(host: str, host_file: str, src_file: str, remove_after_finished: bool ):
    """将一个plot文件转移至目标agent"""
    
    """
    在master启动rsync传输
    """

    import requests
    requests.post("http://localhost:")