# Chia Miner Master

统一管理挖矿主机．在`1min`内为新机器部署挖矿程序.

主机需安装`ubuntu20.04`系统，并启动`openssh-server`服务.

![控制结构](http://processon.com/chart_image/60a6175c5653bb2a26020f82.png)


## 使用方式

### 设备准备

准备一台主机用于运行master控制程序，准备一套`ubuntu20.04`系统的机子，并启动其`openssh-server`服务.

### Master环境安装及配置

在Master机器上安装master依赖 (建议使用虚拟环境)

```
$ pip install -r requirements.txt
```

在`hosts.json`中添加需要控制的矿机，如

``` json
[
    {
        "name": "001", 
        "host": "192.168.10.28", 
        "user": "hzhx", 
        "password": "guangdian523", 
        "workspace": "/home/hzhx/miner-agent"
    }
]
```

| 字段 | 说明 |
| --- | --- |
| name | 该框机名称，在配置文件中需要唯一化．也将用于hpool中显示的矿机名称 |
| host |  |
| user |  |
| password | |
| workspace | 框机中用于存放agent程序的路径 |

### 为矿机安装环境

例如：为001机器安装矿机环境
```
python main.py env install --host 001
```
预计输出
```
cleaning workspace...
H[001] CMD : rm -rf /home/manager/miner-agent
H[001] CMD : mkdir /home/manager/miner-agent
zip and transporting...
ssh closed
installing...
H[001] CMD : unzip -o miner-agent.zip
H[001] CMD : bash install/init-venv.sh
ok
ssh closed
```

若矿机中已经存在agent程序，会被自动覆盖． 
> Tip: 该项目中所有命令皆为无状态命令，可放心重复执行．

为矿机安装好agent程序后，可检查安装状态:

```
python main.py env check --host 001
```
预计输出
```
H[001] CMD : ./check_env.py
{'version': '0.0.1'}
ssh closed
```

### 初始化矿机配置

扫描矿机上的所有的HDD，并约定每个HDD分区中的"{MOUNTPOINT}/plots"目录为hpool-miner的扫盘路径. 最终创建一份"config.yaml"用于挖矿程序．

```
python main.py miner init --host 001
```
预计输出
```
H[001] CMD : ./part_miner_init.py --miner-name=001
ok
ssh closed
```

### 启动挖矿

以"init"阶段生成的配置文件在后台启动挖矿程序.

```
python main.py miner start --host 001
```
预计输出
```
H[001] CMD : ./part_miner_start.py
ok
ssh closed
```

启动后可通过命令检查挖矿状态
```
python main.py miner status --host=001
```
预计输出
```
H[001] CMD : ./part_miner_status.py
----------------
Miner Pid: 49894
+----------+--------+--------+-------------------+-------+------+-------------------------+------------+----------+
| part     | device | fstype | mountpoint        | total | used | plots_dir               | plots_size | configed |
+----------+--------+--------+-------------------+-------+------+-------------------------+------------+----------+
| /dev/sdf | sdf    | ext4   | /media/hzhx/HDD01 | 3.58T | 0.0T | /media/hzhx/HDD01/plots | 0.0T       | True     |
| /dev/sde | sde    | ext4   | /media/hzhx/HDD02 | 3.58T | 0.0T | /media/hzhx/HDD02/plots | 0.0T       | True     |
| /dev/sdd | sdd    | ext4   | /media/hzhx/HDD03 | 3.58T | 0.0T | /media/hzhx/HDD03/plots | 0.0T       | True     |
| /dev/sdc | sdc    | ext4   | /media/hzhx/HDD04 | 3.58T | 0.0T | /media/hzhx/HDD04/plots | 0.0T       | True     |
| /dev/sdb | sdb    | ext4   | /media/hzhx/HDD05 | 3.58T | 0.0T | /media/hzhx/HDD05/plots | 0.0T       | True     |
| /dev/sda | sda    | ext4   | /media/hzhx/HDD06 | 3.58T | 0.0T | /media/hzhx/HDD06/plots | 0.0T       | True     |
+----------+--------+--------+-------------------+-------+------+-------------------------+------------+----------+
ssh closed
```

### 其余功能

请通过`python main.py --help`查看


## 提示
1. P完的图请放在各个HDD分区中的"/plots"路径下'