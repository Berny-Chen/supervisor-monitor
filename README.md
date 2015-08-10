# Supervisor Monitor

基于 Django 的 Supervisor 进程管理工具(python version 2.7)

## 进程管理

![Screenshot] (https://raw.githubusercontent.com/xkuga/supervisor-monitor/master/assets/img/supervisor_index.jpg)

## 配置管理

![Screenshot] (https://raw.githubusercontent.com/xkuga/supervisor-monitor/master/assets/img/supervisor_config.jpg)

## 特性

* 支持 supervisor server 分组管理
* 支持 supervisor server 包含多个配置文件
* 支持常用的进程管理操作，如：重启，停止，查看标准输出日志
* 配置管理：仅支持对 program section 的管理
* 配置同步：采用 scp 命令
* 配置重载：采用 fabric 在目标机器上运行 supervisorctl update 命令

## 配置

* 在 settings.py 中配置 CONFIG_FILE_DIR (本地配置文件的目录，注意权限)
* 在 settings.py 中配置 USER (远程机器的用户)

## SSH

scp 和 fabric 均需要在本地机器和目标机器之间配置 ssh

## Supervisorctl Update

supervisorctl update 默认是需要 sudo 的，因为运行该命令需要对某个 socket 文件有写的权限。
因此只要把这个 socket 文件的所有者改为某个用户，则这个用户就不需要 sudo 也能执行相关命令了。
打开 supervisor 的配置文件，修改如下：

    [unix_http_server]
    chown=kuga:kuga        ; 这里指定 socket 文件的所有者是 kuga
    
## Fixtures

载入 program section 的选项

    python manager.py loaddata section_values

## 本地例子

在 supervisor 的配置文件中加入如下代码:

    [include]
    files = /home/kuga/config/*.conf    ; kuga 要替换为你的用户

在 monitor/fixtures/local_demo.json 中修改 config file path 为:

    "path": "/home/kuga/config/default.conf",

运行 fixtures:

    python manager.py loaddata local_demo
    
本地 supervisor 配置完成

## 终身保修

 ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
